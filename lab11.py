# Intermediate programming practice: async and sockets.
#
# For EACH problem, work out your problem-solving OUTLINE first, then implement it (you
# may use an AI assistant to help - see the README). The async parts must actually run
# their work CONCURRENTLY (that's the whole point), not one after another.
#
# Do not rename the functions - the tests use these names.

import asyncio
import socket

async def gather_doubled(numbers):
    # Outline (write your plan here first):
    #
    # The goal is to double every number in the list and return the results.
    #
    # Example: [1, 2, 3] would return [2, 4, 6]
    #
    # A good way to solve this is by using asyncio.gather.
    # Create a small async function that doubles a number.
    # Run that function for every number at the same time.
    # Return all the results in the same order as the original list.
    #
    # TODO (Part 1, async): run one async task per number that returns n * 2, all
    #   CONCURRENTLY with asyncio.gather, and return the results as a list in the same
    #   order as `numbers`.
    
    async def double(n):
        return n * 2

    results = await asyncio.gather(*(double(n) for n in numbers))

    return results

async def fastest(jobs):
    # Outline:
    #
    # The goal is to find out which job finishes first and return its label.
    #
    # Example: [("A", 3), ("B", 1) would return "B".
    #
    # A good way to solve this is by using asyncio.as_completed.
    # Create an async function that waits for each job's delay.
    # Start all the jobs at the same time using asyncio.create_task.
    # Check which job finishes first and return its label.
    #
    # TODO (Part 2, async): `jobs` is a list of (label, delay) pairs. Start them all
    #   concurrently - each one just does `await asyncio.sleep(delay)` - and return the
    #   label of the FIRST job to finish. (Hint: asyncio.as_completed.)
    
    async def firstJob(label, delay):
        await asyncio.sleep(delay)
        return label

    coros = [firstJob(label, delay) for label, delay in jobs]

    for task in asyncio.as_completed(coros):
        result = await task
        return result

def echo_once(host, port, message):
    # Outline:
    #
    # The goal is to connect to a server, send it a message,
    # and return the reply that the server sends back.
    #
    # Example: Sending "Hello" to an echo server should return "Hello".
    #
    # A good way to solve this is by using a TCP socket.
    # Connect to the server using the host and port.
    # Convert the message into bytes and send it.
    # Recieve the server's reply and convert it back into a string.
    # Return the reply and close the socket when finished.
    #
    # TODO (Part 3, sockets): open a TCP socket and connect to (host, port). Send
    #   `message` (encode it to bytes first), receive the server's reply, and return it
    #   as a string. (Hint: socket.socket, .connect, .sendall, .recv, .decode.)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())

        data = s.recv(1024)

        return data.decode()

def main():
    # Optional scratch space - try the async parts here, e.g.:
    print(asyncio.run(gather_doubled([1, 2, 3, 4])))   # [2, 4, 6, 8]
    print(asyncio.run(fastest([("A", 0.06), ("B", 0.02), ("C", 0.04)])))    # returns "B"
    print(echo_once("127.0.0.1", 50011, "hello"))   # returns "hello"   (against an echo server)
    
if __name__ == "__main__":
    main()