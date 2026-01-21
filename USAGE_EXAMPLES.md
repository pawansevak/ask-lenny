# Ask Lenny - Usage Examples

## Example 1: Basic Query

```python
from rag_system import LennyRAG

# Initialize
rag = LennyRAG()

# Ask a question
result = rag.ask("What causes analytics projects to fail?")

# Print answer
print(result['answer'])

# Print citations
for citation in result['citations']:
    print(f"- {citation['guest']}: {citation['title']}")
```

## Example 2: Export to Markdown

```python
from rag_system import LennyRAG

rag = LennyRAG()
result = rag.ask("How long does it take to build trust in data?")

# Export to markdown
markdown = rag.export_to_markdown(result)

# Save to file
with open("trust_in_data.md", "w") as f:
    f.write(markdown)
```

## Example 3: Batch Queries

```python
from rag_system import LennyRAG

rag = LennyRAG()

queries = [
    "What causes analytics projects to fail?",
    "Build vs buy analytics platforms",
    "Schema evolution challenges",
    "Data governance at scale"
]

results = []
for query in queries:
    print(f"Querying: {query}")
    result = rag.ask(query, n_results=10)
    results.append(result)
    
# Save all results
with open("batch_results.md", "w") as f:
    for result in results:
        f.write(rag.export_to_markdown(result))
        f.write("\n\n---\n\n")
```

## Example 4: Custom Analysis for CJA

```python
from rag_system import LennyRAG

rag = LennyRAG()

# CJA-specific queries
cja_queries = [
    "What are the hidden costs of building analytics in-house?",
    "Why do companies switch analytics platforms?",
    "Data quality challenges at enterprise scale",
    "Metric consistency across teams",
    "Analytics governance and compliance",
    "Schema migration and evolution",
    "Building trust in analytics systems"
]

# Create comprehensive report
report = "# CJA Competitive Intelligence Report\n\n"
report += "Source: Lenny's Podcast (269 episodes)\n\n"

for i, query in enumerate(cja_queries):
    print(f"Processing query {i+1}/{len(cja_queries)}: {query}")
    
    result = rag.ask(query, n_results=15)
    
    report += f"## {i+1}. {query}\n\n"
    report += result['answer'] + "\n\n"
    report += f"*Based on {result['n_sources']} sources*\n\n"
    report += "---\n\n"

# Save report
with open("cja_competitive_intelligence.md", "w") as f:
    f.write(report)

print("✅ Report saved to cja_competitive_intelligence.md")
```

## Example 5: Interactive Mode

```python
from rag_system import LennyRAG

rag = LennyRAG()

print("Ask Lenny - Interactive Mode")
print("=" * 50)
print("Type 'quit' to exit\n")

while True:
    query = input("Your question: ")
    
    if query.lower() in ['quit', 'exit', 'q']:
        break
    
    if not query.strip():
        continue
    
    print("\nSearching...\n")
    result = rag.ask(query)
    
    print("Answer:")
    print(result['answer'])
    print(f"\nBased on {result['n_sources']} sources")
    print("-" * 50)
    print()
```

## Example 6: Search Only (No Synthesis)

```python
from rag_system import LennyRAG

rag = LennyRAG()

# Just search, don't synthesize
search_results = rag.search("data quality", n_results=5)

for i, chunk in enumerate(search_results['chunks']):
    print(f"\n[Result {i+1}]")
    print(f"Guest: {chunk['metadata']['guest']}")
    print(f"Episode: {chunk['metadata']['title']}")
    print(f"Relevance: {1 - chunk['distance']:.2%}")
    print(f"\nExcerpt:")
    print(chunk['text'][:300] + "...")
```

## Example 7: Filter by Guest

```python
from rag_system import LennyRAG

rag = LennyRAG()

# Search with a specific guest in mind
result = rag.ask("What does Vijay Iyengar say about data quality?", n_results=15)

print(result['answer'])

# Check which guests were cited
guests = [c['guest'] for c in result['citations']]
print(f"\nGuests cited: {', '.join(set(guests))}")
```

## Example 8: Time-based Analysis

```python
from rag_system import LennyRAG
from datetime import datetime

rag = LennyRAG()

# Get all results
result = rag.ask("What causes analytics projects to fail?", n_results=20)

# Analyze by publish date
dates = []
for chunk in result['raw_chunks']:
    date_str = chunk['metadata'].get('publish_date')
    if date_str:
        dates.append(date_str)

print("Episodes by year:")
from collections import Counter
years = [d[:4] for d in dates]
for year, count in Counter(years).most_common():
    print(f"  {year}: {count} episodes")
```

## Common Use Cases

### For CJA Project:

```python
# Live objection handling
result = rag.ask("What about schema migration in analytics?")

# Competitive intelligence
result = rag.ask("Why did companies switch from Mixpanel?")

# Deep dive on specific topic
result = rag.ask("Data governance challenges", n_results=20)

# Get all quotes from a company
result = rag.ask("What do Stripe leaders say about metrics?")
```

### For Sales Enablement:

```python
# Customer objections
result = rag.ask("Why not build analytics in-house?")

# Success stories
result = rag.ask("How did companies scale their analytics?")

# Pain points
result = rag.ask("What frustrates teams about DIY analytics?")
```

### For Product Strategy:

```python
# Feature priorities
result = rag.ask("Most requested analytics features")

# User needs
result = rag.ask("What do product teams need from analytics?")

# Market trends
result = rag.ask("Future of product analytics")
```

## Tips

1. **Be Specific**: "Data quality" vs "Data quality challenges in mobile analytics"
2. **Use Context**: Add role/company context to queries
3. **Iterate**: Refine queries based on initial results
4. **Combine Results**: Ask multiple related questions for comprehensive analysis
5. **Export Everything**: Save results for future reference
