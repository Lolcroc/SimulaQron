A simple version of BB84 for extracting 1 bit of key.

Creators:
Yves van Montfort, TU Delft student No. 4388909
Thomas Roggen, TU Delft student No. 4494539

### How to run
In $NETSIM/config/settings.ini, set: maxqubits_per_node = 256

```
sh $NETSIM/run/startAll.sh --nodes "Alice Bob Eve"
sh run_example.sh
```

### There are 2 command-line arguments to modify the behaviour:

-n [xxx]    Run with [xxx] input bits. Standard behaviour is 16, but no more than 256
-E          Activate the eavesdropper Eve. She will measure all qubits going from Alice to Bob

### Examples

$ sh run_example.sh

    Expected output:
    Running w/ 16 input bits, Eve active: [n]

    $ Eve done
    Alice's delta error: 0.0
    Alice made key = 0
    Alice done
    Bob's delta error: 0.0
    Bob made key = 0
    Bob done

$ sh run_example -E

    Expected output:
    Running w/ 16 input bits, Eve active: [y]

    $ Eve done
    Alice's delta error: 0.2
    Alice aborted protocol
    Alice done
    Bob's delta error: 0.2
    Bob aborted protocol
    Bob done

$ sh run_example -E -n 100

    Expected output:
    Running w/ 100 input bits, Eve active: [y]

    $ Eve done
    Bob's delta error: 0.25
    Bob aborted protocol
    Bob done
    Alice's delta error: 0.25
    Alice aborted protocol
    Alice done