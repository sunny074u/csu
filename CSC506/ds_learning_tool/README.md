# Data Structure Learning Tool

## What this tool does
- Implements Stack, Queue, and Singly Linked List
- Interactive UI that demonstrates operations
- Complexity analyzer showing Big-O predictions
- Performance benchmarking comparing predicted vs actual scaling
- Report outputs and charts

## Run the UI
pip install -r requirements.txt
streamlit run app.py

## Run performance tests + report
python benchmark.py
python report.py

## Output files
- outputs/benchmark_results.csv
- outputs/prediction_accuracy.csv
- outputs/chart_stack.png
- outputs/chart_queue.png
- outputs/chart_linkedlist.png
- outputs/accuracy_overview.png
- outputs/report.md
