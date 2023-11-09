# bioasq11b-pubic
Public code for Macquarie University's participation at bioASQ 11b

## What is this repository for? ###

This code implements Macquarie University's experiments and
participation in BioASQ 11b.
* [BioASQ](http://www.bioasq.org)


## How do I get set up? ###

Apart from the code in this repository, you will need the following files:

* `BioASQ-training11b/training11b.json` - available from [BioASQ](http://www.bioasq.org/)

## Reading

If you use this code, please cite the following paper:

TBA

## Examples of runs

The following runs can be made with the files available in this repository:

```
  python GPTZero.py -t BioASQ-task11bPhaseB-testset1.json
```

```
  python GPTWithContext.py -t BioASQ-task11bPhaseB-testset1.json
```

The following run will also require the file `BioASQ-training11b/training11b.json`:

```
  python GPTNoContext.py -t BioASQ-task11bPhaseB-testset1.json
```

The following runs will require the output of an existing summariser. We used the summariser available in https://github.com/dmollaaliod/bioasq10b-public and we have included its output for your convenience. The output will need to be saved in the file `MQ5-DistilBERT.json`:

```
python GPTBioASQ10bContext.py -t BioASQ-task11bPhaseB-testset4.json -c MQ5-DistilBERT.json
```

```
python GPTBioASQ10bFewShotContext.py -t BioASQ-task11bPhaseB-testset4.json -c MQ5-DistilBERT.json
```

(`GPTBioASQ10bFewShotContext.py` also requires `Task10BGoldenEnriched/10B2_golden.json` and the output of a summariser on that file; edit lines 14 and 15 accordingly. Again, we used https://github.com/dmollaaliod/bioasq10b-public and we have included its output for your convenience)

## Who do I talk to?

Diego Molla: [diego.molla-aliod@mq.edu.au](mailto:diego.molla-aliod@mq.edu.au)
