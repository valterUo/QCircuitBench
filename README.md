# Extended and simplified QCircuitBench dataset

This fork reorganizes QCircuitBench into a Python module that can be installed as

```
pip install git+https://github.com/valterUo/QCircuitBench.git
```

Some of the original features are removed and this version focuses on circuit generation. Moreover, many new algorithms are added from:

1. [Qrisp](https://qrisp.eu/reference/Algorithms/index.html)
2. [Cirq examples](https://github.com/quantumlib/Cirq/tree/main/examples)
3. [Quantum algorithm zoo](https://quantumalgorithmzoo.org/)
4. [Classiq algorithms library](https://github.com/Classiq/classiq-library/tree/main/algorithms)
5. [MQT (Munich Quantum Toolkit) Bench](https://mqt-bench.app/)
6. [Quantum circuit generation repo](https://github.com/teaguetomesh/quantum_circuit_generator)

There is no quarantee that every detail is correct currently but we will work on checking the details. The code also focuses on the fact that these circuits can easily be used as an input for a machine learning and especially LLM fine-tuning.

Example usage:

```python
import qcircuitbench

# Show a complete record
rec = qcircuitbench.get('grover', n_qubits=3)
print('=== GROVER (3 qubits) ===')
print('Description:', rec.description[:200])
print('Pattern:', rec.pattern_description[:200])
print('Parameters:', rec.parameters)
print('Difficulty:', rec.difficulty)
print('Category:', rec.category)
print()
print('QASM:')
print(rec.qasm[:500])
print()

# Test search
print('Search \"factor\":', qcircuitbench.search('factor'))
print('Search \"error\":', qcircuitbench.search('error'))
print('Search \"walk\":', qcircuitbench.search('walk'))
print()

# Test get_all by category
recs = qcircuitbench.get_all(category='error_correction', n_qubits=5)
print('Error correction circuits:', [r.name for r in recs])
recs = qcircuitbench.get_all(category='state_preparation', n_qubits=4)
print('State prep circuits:', [r.name for r in recs])
```

or

```python
from qcircuitbench.export import to_jsonl, to_qasm_dir
import json

# Export training JSONL
n = to_jsonl('/tmp/qcb_test/train.jsonl', qubit_range=range(2, 6))
print(f'Exported {n} training records to JSONL')

# Show first record
with open('/tmp/qcb_test/train.jsonl') as f:
    first = json.loads(f.readline())
print()
print('=== First training record ===')
print('Prompt (first 300 chars):')
print(first['prompt'][:300])
print()
print('Completion (first 200 chars):')
print(first['completion'][:200])
print()
print('Metadata keys:', list(first['metadata'].keys()))

# Export QASM directory
n2 = to_qasm_dir('/tmp/qcb_test/qasm_export', qubit_range=range(3, 5))
print(f'Exported {n2} QASM files')
```


# 📚 Citation

If you use QCircuitBench in your work, please cite:

```bibtex
@inproceedings{yang2025qcircuitbench,
  title={QCircuitBench: A Large-Scale Dataset for Benchmarking Quantum Algorithm Design},
  author={Yang, Rui and Wang, Ziruo and Gu, Yuntian and Liang, Yitao and Li, Tongyang},
  booktitle={The Thirty-ninth Annual Conference on Neural Information Processing Systems (NeurIPS 2025), Datasets and Benchmarks Track},
  year={2025},
  url={https://arxiv.org/abs/2410.07961}
}
```