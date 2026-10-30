Application-Side Technical Documentation
========================================

Document category
    Application development
Platform
    Linux-based embedded systems
Communication interface
    Ethernet
Communication protocol
    TCP/IP
Programming language
    Python 3
Application
    Network connectivity and data exchange

Introduction
------------

Ethernet communication is widely used in embedded Linux systems to exchange
data between devices over a wired network. It provides a standard
communication interface for embedded devices, computers, controllers,
gateways, and other network-enabled equipment.

Applications on different devices can exchange information using network
protocols such as TCP (Transmission Control Protocol) and UDP (User Datagram
Protocol). This guide explains how to verify Ethernet connectivity and
implement basic TCP/IP communication between two Linux-based devices using
Python socket programming.

The procedures are adaptable across Linux-based embedded platforms and do not
depend on a specific processor, development board, or Ethernet controller.

Objectives
----------

This guide covers how to:

* Verify that an Ethernet interface is available.
* Check network connectivity and IP address configuration.
* Establish a TCP connection between applications.
* Transmit and receive application data.
* Monitor communication status and handle errors.
* Validate successful data exchange and troubleshoot common problems.

Scope
-----

The guide focuses on application-level Ethernet communication using TCP/IP on
Linux-based systems. It covers Ethernet interface verification, IP and network
configuration, connectivity testing, TCP client/server applications, message
handling, deployment, monitoring, and troubleshooting.

The examples use the Python standard library and require no external
communication framework.

Ethernet Communication Architecture
-----------------------------------

Devices connected to the same network, or to appropriately routed networks,
can exchange data using IP. Each device must have a valid IP configuration.

For TCP communication, one application acts as a server and listens for
incoming connections. A client connects to that server using its IP address
and port number.

Device roles
~~~~~~~~~~~~

**Device A - TCP server**

* Binds to a listening IP address and port.
* Waits for client connections.
* Receives and processes application messages.
* Sends a response to the client.

**Device B - TCP client**

* Connects to the server's IP address and port.
* Sends application data and receives the server response.
* Closes the connection when communication is complete.

Data flow
~~~~~~~~~

::

   Device B (TCP client) -> Ethernet network -> Device A (TCP server)
   Device A (TCP server) -> Ethernet network -> Device B (TCP client)

Example network configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following addresses are examples. Use addresses that match the target
network.

.. list-table::
   :header-rows: 1
   :widths: 25 35 35

   * - Parameter
     - Device A (server)
     - Device B (client)
   * - Device role
     - TCP server
     - TCP client
   * - IP address
     - ``192.168.10.100``
     - ``192.168.10.101``
   * - Subnet mask
     - ``255.255.255.0``
     - ``255.255.255.0``
   * - TCP port
     - ``5000``
     - ``5000``
   * - Protocol
     - TCP
     - TCP

TCP/IP communication
~~~~~~~~~~~~~~~~~~~~

TCP is a connection-oriented transport protocol. The client establishes a
connection before exchanging data. TCP provides reliable, ordered byte-stream
delivery, error detection and retransmission, flow control, and connection
termination.

TCP does not preserve application message boundaries. Applications must define
their own message framing. The examples in this guide use newline-delimited
JSON messages, with one message per line.

Ethernet Interface Verification
-------------------------------

Before implementing TCP communication, verify that the Ethernet interface is
available and configured. Linux networking utilities can show interface
status, IP addresses, routes, and link state.

Identify available network interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run:

.. code-block:: console

   ip link show

Example output:

.. code-block:: text

   1: lo: <LOOPBACK,UP,LOWER_UP>
   2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>

The interface name varies by platform. Common names include ``eth0``,
``eth1``, ``enp1s0``, and ``end0``. Use the name reported by the system.

Check Ethernet interface status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inspect an interface:

.. code-block:: console

   ip link show eth0

Replace ``eth0`` with the actual interface name. To enable or disable an
interface manually:

.. code-block:: console

   sudo ip link set eth0 up
   sudo ip link set eth0 down

Bringing an interface up does not automatically assign an IP address.

Check IP address configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display all addresses, or inspect a specific interface:

.. code-block:: console

   ip addr show
   ip addr show eth0

Example output:

.. code-block:: text

   2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
       inet 192.168.10.100/24
       scope global eth0

The ``inet`` entry displays the configured IPv4 address and network prefix.

Check network routing
~~~~~~~~~~~~~~~~~~~~~

Run:

.. code-block:: console

   ip route show

Example output:

.. code-block:: text

   192.168.10.0/24 dev eth0 proto kernel scope link
   default via 192.168.10.1 dev eth0

The routing table determines how packets are forwarded. Devices in the same
subnet normally communicate through a direct route. Communication with other
networks requires an appropriate gateway or route.

Check Ethernet link status
~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``ethtool`` is installed, inspect the link:

.. code-block:: console

   ethtool eth0

Example output:

.. code-block:: text

   Settings for eth0:
       Speed: 1000Mb/s
       Duplex: Full
       Auto-negotiation: on
       Link detected: yes

The actual speed and duplex mode depend on the Ethernet hardware and connected
network equipment. ``Link detected`` indicates whether the physical link is
detected.

IP Address Configuration
------------------------

Devices need IP addresses to identify and communicate with one another. A
device can receive its configuration dynamically through DHCP or use a
manually configured static address.

DHCP configuration
~~~~~~~~~~~~~~~~~~

DHCP (Dynamic Host Configuration Protocol) automatically provides network
configuration. Depending on the Linux distribution, DHCP may be managed by
NetworkManager, systemd-networkd, or another network service.

If ``dhclient`` is installed and is the configured mechanism, request a lease
and then check the assigned address:

.. code-block:: console

   sudo dhclient eth0
   ip addr show eth0

Do not run multiple network configuration services simultaneously on the same
interface. Use the network manager configured for the target system.

Static IP address configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a direct two-device test, temporary static addresses can be added as
follows.

On Device A:

.. code-block:: console

   sudo ip addr add 192.168.10.100/24 dev eth0

On Device B:

.. code-block:: console

   sudo ip addr add 192.168.10.101/24 dev eth0

Enable the interface if required and verify the address:

.. code-block:: console

   sudo ip link set eth0 up
   ip addr show eth0

These commands add addresses temporarily; they do not configure persistent
network settings. For permanent configuration, use the network management
mechanism supported by the Linux distribution.

Verify network configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On both devices, check the addresses and routes:

.. code-block:: console

   ip addr show
   ip route show

For the example configuration, Device A (``192.168.10.100/24``) and Device B
(``192.168.10.101/24``) are both in the ``192.168.10.0/24`` network.

Network Connectivity Testing
----------------------------

After configuring the interfaces and addresses, verify that the devices can
communicate over the network.

Test connectivity using ping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From Device A, send four ICMP echo requests to Device B:

.. code-block:: console

   ping -c 4 192.168.10.101

Successful output indicates that Device A is receiving ICMP responses from
Device B. Test the reverse direction from Device B:

.. code-block:: console

   ping -c 4 192.168.10.100

Understand ping results
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Result
     - Meaning
     - Recommended action
   * - Successful ping
     - Destination responds to ICMP requests.
     - Continue with TCP testing.
   * - Destination Host Unreachable
     - Destination cannot currently be reached.
     - Check IP configuration, subnet, and physical connectivity.
   * - Request timed out
     - No ICMP response was received before the timeout.
     - Check network connectivity and firewall rules.
   * - Network unreachable
     - No suitable route is available.
     - Verify the routing table and gateway configuration.

A successful ping confirms ICMP connectivity, but does not guarantee that a
TCP service is listening or reachable. Test TCP communication separately.

TCP Server Implementation
-------------------------

The server listens on TCP port ``5000``, receives newline-delimited JSON
messages, displays the received data, and sends an acknowledgement. This simple
example handles one connected client at a time.

Create a Python file named ``tcp_server.py``. The server creates and binds a
socket, listens for connections, accepts a client, decodes and validates JSON
messages, sends acknowledgements, and continues until the client disconnects.

Complete server code
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """TCP server for receiving application data from remote Linux devices."""

   import json
   import socket

   SERVER_HOST = "0.0.0.0"
   SERVER_PORT = 5000
   BUFFER_SIZE = 4096


   def process_message(message):
       """Process a received JSON message."""
       try:
           data = json.loads(message)
       except json.JSONDecodeError:
           return {
               "status": "error",
               "message": "Invalid JSON data",
           }

       print("\nReceived application data:")
       print(json.dumps(data, indent=4))
       return {
           "status": "success",
           "message": "Data received successfully",
       }


   def handle_client(client_socket, client_address):
       """Handle communication with one connected client."""
       print("\nClient connected:", client_address)
       buffer = b""

       try:
           while True:
               received = client_socket.recv(BUFFER_SIZE)
               if not received:
                   print("Client disconnected:", client_address)
                   break

               buffer += received
               while b"\n" in buffer:
                   raw_message, buffer = buffer.split(b"\n", 1)
                   if not raw_message:
                       continue

                   try:
                       message = raw_message.decode("utf-8")
                   except UnicodeDecodeError:
                       response = {
                           "status": "error",
                           "message": "Invalid UTF-8 data",
                       }
                   else:
                       response = process_message(message)

                   response_data = (
                       json.dumps(response) + "\n"
                   ).encode("utf-8")
                   client_socket.sendall(response_data)
       except OSError as error:
           print("Client communication error:", error)
       finally:
           client_socket.close()
           print("Client connection closed.")


   def main():
       server_socket = socket.socket(
           socket.AF_INET,
           socket.SOCK_STREAM,
       )
       server_socket.setsockopt(
           socket.SOL_SOCKET,
           socket.SO_REUSEADDR,
           1,
       )

       try:
           server_socket.bind((SERVER_HOST, SERVER_PORT))
           server_socket.listen(5)
           print("TCP server started.")
           print("Listening on port:", SERVER_PORT)

           while True:
               client_socket, client_address = server_socket.accept()
               handle_client(client_socket, client_address)
       except KeyboardInterrupt:
           print("\nTCP server stopped.")
       except OSError as error:
           print("Server error:", error)
       finally:
           server_socket.close()


   if __name__ == "__main__":
       main()

Server configuration
~~~~~~~~~~~~~~~~~~~~

``SERVER_HOST = "0.0.0.0"`` makes the server listen on all available IPv4
interfaces. Configure a specific local IP address if the server should listen
on only one interface. Since listening on all interfaces can expose the port
more broadly, restrict access using the device's network and firewall policy.

``SERVER_PORT = 5000`` defines the port to which the client connects. The
``socket.AF_INET`` and ``socket.SOCK_STREAM`` arguments select an IPv4 TCP
socket. ``bind`` associates the socket with the configured address and port;
``listen(5)`` places it in listening mode with a requested connection backlog.
``accept`` waits for an incoming connection.

The server buffers received bytes and processes each complete newline-terminated
message. In a production application, also define an application-specific
maximum message size and validate the expected JSON fields and types.

TCP Client Implementation
-------------------------

The client connects to the server using its IP address and port. It sends JSON
application data and waits for an acknowledgement.

Create a Python file named ``tcp_client.py``. The client creates a TCP socket,
connects to the server, generates and sends application data, receives the
server response, and repeats transmission at the configured interval.

Complete client code
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """TCP client for sending application data to a remote Linux device."""

   import json
   import socket
   import time

   SERVER_IP = "192.168.10.100"
   SERVER_PORT = 5000
   INTERVAL = 5
   BUFFER_SIZE = 4096


   def generate_application_data():
       """Generate example application data."""
       return {
           "device": "Linux_Device_01",
           "temperature": 28.5,
           "humidity": 62.0,
           "status": "normal",
       }


   def receive_response(response_stream):
       """Read one newline-terminated server response."""
       response = response_stream.readline()
       if not response:
           raise ConnectionError("Server closed the connection")
       return response.decode("utf-8")


   def main():
       client_socket = socket.socket(
           socket.AF_INET,
           socket.SOCK_STREAM,
       )
       client_socket.settimeout(10)
       response_stream = None

       try:
           print("Connecting to TCP server...")
           client_socket.connect((SERVER_IP, SERVER_PORT))
           response_stream = client_socket.makefile("rb")
           print("Connected to server:", SERVER_IP, SERVER_PORT)

           while True:
               application_data = generate_application_data()
               message = (
                   json.dumps(application_data) + "\n"
               ).encode("utf-8")
               client_socket.sendall(message)

               print("\nSent data:")
               print(json.dumps(application_data, indent=4))

               response = receive_response(response_stream)
               print("\nServer response:")
               print(json.dumps(json.loads(response), indent=4))

               time.sleep(INTERVAL)
       except KeyboardInterrupt:
           print("\nTCP client stopped.")
       except (OSError, ValueError) as error:
           print("Communication error:", error)
       finally:
           if response_stream is not None:
               response_stream.close()
           client_socket.close()
           print("Client socket closed.")


   if __name__ == "__main__":
       main()

The response stream reads through the newline delimiter, preserving any
subsequent buffered bytes. This is important because TCP is a byte stream and
one ``recv`` call is not guaranteed to correspond to one application message.

Client configuration
~~~~~~~~~~~~~~~~~~~~

* ``SERVER_IP`` is the IP address of the device running the server. Replace
  ``192.168.10.100`` with the actual server address.
* ``SERVER_PORT`` must match the server's configured port.
* ``socket.AF_INET`` and ``socket.SOCK_STREAM`` create an IPv4 TCP socket.
* ``connect`` establishes the connection, and ``sendall`` transmits the
  complete encoded message.
* ``receive_response`` reads the server's newline-terminated acknowledgement.

Application Deployment and Execution
------------------------------------

The applications can run on two Linux-based devices connected through an
Ethernet network. The examples use only Python standard-library modules.

Application directory structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the following files:

.. code-block:: text

   ethernet_application/
   ├── tcp_server.py
   └── tcp_client.py

Verify Python installation
~~~~~~~~~~~~~~~~~~~~~~~~~~

On both devices, confirm that Python 3 is available:

.. code-block:: console

   python3 --version

Configure and start the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure Device A with the server address (``192.168.10.100`` in this
example), and verify its interface using ``ip addr show``. Start the server:

.. code-block:: console

   python3 tcp_server.py

Expected output:

.. code-block:: text

   TCP server started.
   Listening on port: 5000

The server is now waiting for client connections.

Configure and start the client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure Device B with an address in the same network (``192.168.10.101`` in
this example). In ``tcp_client.py``, verify that the server settings match
Device A:

.. code-block:: python

   SERVER_IP = "192.168.10.100"
   SERVER_PORT = 5000

Start the client on Device B:

.. code-block:: console

   python3 tcp_client.py

The client connects to the server and begins transmitting application
messages.

Expected Output and Data Validation
-----------------------------------

When the TCP connection succeeds, the server should receive application data
from the client.

Example server output
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   TCP server started.
   Listening on port: 5000

   Client connected: ('192.168.10.101', 45678)

   Received application data:
   {
       "device": "Linux_Device_01",
       "temperature": 28.5,
       "humidity": 62.0,
       "status": "normal"
   }

The source port is assigned dynamically and may differ.

Example client output
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Connecting to TCP server...
   Connected to server: 192.168.10.100 5000

   Sent data:
   {
       "device": "Linux_Device_01",
       "temperature": 28.5,
       "humidity": 62.0,
       "status": "normal"
   }

   Server response:
   {
       "status": "success",
       "message": "Data received successfully"
   }

The client continues sending messages every five seconds.

Message format
~~~~~~~~~~~~~~

The client sends JSON because it provides a structured format for multiple
data fields. The message is terminated by a newline (``\n``), which provides
message framing over the TCP byte stream.

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Field
     - Description
     - Example
   * - ``device``
     - Identifies the sending device.
     - ``Linux_Device_01``
   * - ``temperature``
     - Temperature measurement.
     - ``28.5``
   * - ``humidity``
     - Relative humidity measurement.
     - ``62.0``
   * - ``status``
     - Application status.
     - ``normal``

Validation checklist
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Test case
     - Expected result
   * - Ethernet interface verification
     - Interface is available and enabled.
   * - IP address configuration
     - Correct IP address is assigned.
   * - Network connectivity
     - Devices can communicate over the network.
   * - TCP server initialization
     - Server starts and listens on the configured port.
   * - TCP client connection
     - Client establishes a connection with the server.
   * - Data transmission
     - Client sends application data successfully.
   * - Data reception
     - Server receives the complete message.
   * - JSON processing
     - Server decodes the received message.
   * - Server response
     - Client receives an acknowledgement.
   * - Connection termination
     - Client and server close sockets correctly.

Network and TCP Communication Monitoring
-----------------------------------------

Linux provides utilities to monitor Ethernet interfaces and TCP connections.

Check active TCP connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display active connections and listening TCP ports:

.. code-block:: console

   ss -tn
   ss -ltn

To check whether port ``5000`` is listening:

.. code-block:: console

   ss -ltnp | grep 5000

Check network statistics
~~~~~~~~~~~~~~~~~~~~~~~~

Inspect interface statistics, including transmitted and received packets and
errors:

.. code-block:: console

   ip -s link show eth0

Replace ``eth0`` with the actual interface name.

Monitor TCP traffic
~~~~~~~~~~~~~~~~~~~

If ``tcpdump`` is installed, capture traffic associated with port ``5000``:

.. code-block:: console

   sudo tcpdump -i eth0 tcp port 5000

Press ``Ctrl+C`` to stop the capture. Packet captures can help identify
connection attempts, transmitted data, retransmissions, and communication
failures. They may also contain application data; handle capture files
according to applicable security and privacy requirements.

Error Handling and Communication Reliability
--------------------------------------------

Communication can fail because of physical connection problems, incorrect IP
configuration, unavailable services, or application errors. Applications
should detect and report failures clearly.

Connection refused
~~~~~~~~~~~~~~~~~~

A connection-refused error may occur when the server is not running, the client
uses the wrong port, the server is not listening on the expected address, or a
firewall actively rejects the connection.

Check whether the server is listening:

.. code-block:: console

   ss -ltnp | grep 5000

Connection timeout
~~~~~~~~~~~~~~~~~~

A timeout may occur when the destination is unreachable, routing is incorrect,
a firewall drops packets, or the remote device is not responding. Check
connectivity and verify the IP address and network configuration:

.. code-block:: console

   ping -c 4 192.168.10.100

Connection closed
~~~~~~~~~~~~~~~~~

A connection may close when the server or client terminates its socket.
Applications should detect a closed connection and release associated
resources. Long-running applications may implement a reconnect mechanism to
recover after temporary network failures.

Invalid application data
~~~~~~~~~~~~~~~~~~~~~~~~

Messages may contain malformed JSON or unexpected fields. Validate incoming
data before processing it. For example:

.. code-block:: python

   import json

   message = '{"temperature": 28.5}'

   try:
       data = json.loads(message)
       print("Received:", data)
   except json.JSONDecodeError:
       print("Invalid JSON message")

Validation helps prevent incorrect application data from being processed.

Troubleshooting
---------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Issue
     - Possible cause
     - Recommended action
   * - Ethernet interface not visible
     - Driver or interface configuration issue.
     - Check available interfaces using ``ip link show``.
   * - Ethernet link not detected
     - Cable or network equipment issue.
     - Check the physical connection and link status.
   * - No IP address assigned
     - DHCP failure or missing static configuration.
     - Verify the network configuration.
   * - Ping unsuccessful
     - Incorrect IP, routing issue, or blocked ICMP.
     - Check IP addresses, subnet, routes, and firewall settings.
   * - TCP connection refused
     - Server is not listening.
     - Start the TCP server and verify its port.
   * - TCP connection timeout
     - Network path or firewall issue.
     - Check connectivity and firewall rules.
   * - Data not received
     - Incorrect destination or application framing.
     - Verify client/server configuration and message format.
   * - Invalid JSON error
     - Malformed application message.
     - Validate the JSON payload before transmission.
   * - Connection unexpectedly closed
     - Remote application terminated or network failure.
     - Inspect application logs and connection handling.
   * - TCP port unavailable
     - Another application is using the port.
     - Check active listening sockets using ``ss``.

Useful diagnostic commands
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   ip link show
   ip addr show
   ip route show
   ping -c 4 192.168.10.100
   ss -ltnp
   dmesg | tail -50

These commands help identify common Ethernet and TCP communication problems.

Security Considerations
-----------------------

Configure Ethernet communication according to the application's security
requirements. Recommended practices include:

* Use only the required TCP ports.
* Restrict incoming connections using firewall rules.
* Validate received application data.
* Avoid transmitting passwords or sensitive credentials in plain text.
* Use authenticated and encrypted communication for sensitive information.
* Restrict server access to trusted network devices.
* Monitor communication errors and unexpected connection attempts.
* Avoid exposing application listening ports to untrusted networks.

The Python example uses plain TCP and does not provide encryption or client
authentication. For production systems exchanging sensitive information, use
an appropriate secure transport such as TLS and implement suitable peer
authentication.

Conclusion
----------

Ethernet communication provides a standard method for exchanging data between
Linux-based embedded systems and other network-enabled devices. Python socket
programming can establish TCP connections, transmit structured application
data, receive responses, and monitor communication status.

The client/server example can be adapted to different embedded Linux
platforms and application requirements. The network verification procedures
and diagnostic commands provide a foundation for identifying Ethernet
connectivity and communication problems.

References
----------

* `Python Socket Programming Documentation
  <https://docs.python.org/3/library/socket.html>`_
* `Linux IP Command Manual <https://man7.org/linux/man-pages/man8/ip.8.html>`_
* `Linux SS Command Manual <https://man7.org/linux/man-pages/man8/ss.8.html>`_
* `Linux Ping Command Manual
  <https://man7.org/linux/man-pages/man8/ping.8.html>`_
* `TCP Protocol - RFC 9293 <https://www.rfc-editor.org/rfc/rfc9293>`_
* `Internet Protocol Version 4 - RFC 791
  <https://www.rfc-editor.org/rfc/rfc791>`_
