import argparse
import serial
import time
import sys
import monitoring
from metrics import generate_metrics

parser = argparse.ArgumentParser(description='Send performance statistics over a serial port')
parser.add_argument("serial_port", type=str, help="serial port to output to or 'stdout'", nargs='?')
parser.add_argument("--polling_rate", metavar="n", type=int, default=4, help="number of times per second to process statistics (default: 24)")
parser.add_argument("--sma_samples", metavar="n", type=int, default=8, help="number of times per second to process statistics (default: 12)")
parser.add_argument("--connect_timeout", metavar="n", type=float, default=1, help="number of times per second to process statistics (default: 12)")

def connect(port, access_timeout, connect_timeout):
  ser = None
  while not ser:
    try:
      ser = serial.Serial(port, timeout=access_timeout, write_timeout=access_timeout)
    except Exception as e:
      print(e, file=sys.stderr)
      time.sleep(connect_timeout)
  return ser

def send(string, ser):
  for message in string.splitlines():
    bytes = message.encode("utf-8") + b"\r"
    ser.write(bytes)
    ser.flush()
    echo = ser.read(len(bytes) + 1)
    assert bytes + b"\n" == echo, "controller didn't echo back"

def main():
  args = parser.parse_args()
  metrics = generate_metrics(args.sma_samples)
  if args.serial_port:
    ser = connect(args.serial_port, 1/args.polling_rate, args.connect_timeout)
  while True:
    for metric, func in metrics.items():
      data = func()
      if data:
        message = "%s %s" % (metric, " ".join(map(repr, func())))
        if args.serial_port:
          try:
            send(message, ser)
          except Exception as e:
            print(e, file=sys.stderr)
            ser.close()
            ser = connect(args.serial_port, 1/args.polling_rate, args.connect_timeout)
        else:
          print(message)
    time.sleep(1/args.polling_rate)
    monitoring.update()

if __name__ == "__main__":
  main()
