# Week 4 - LangChain

## Day 1 - LangChain Architecture


## What is LangChain?

LangChain is a framework for building applications powered by Large Language Models.

It provides abstractions for:

- Models
- Prompts
- Chains
- Retrievers
- Tools
- Agents
- Memory


## Raw API vs LangChain


### Raw API


Application

|

Provider SDK

|

LLM

|

Answer



### LangChain


Application

|

PromptTemplate

|

ChatModel

|

Chain

|

Answer



## ChatModel

ChatModel is an abstraction over chat-based LLMs.

Example:

```python
ChatOpenAI()

Instead of directly calling provider APIs, LangChain provides a unified interface:

model.invoke(messages)
Messages

LangChain uses structured messages:

SystemMessage

Defines model behavior.

Example:

You are an AI research assistant.
HumanMessage

Represents user input.

Example:

Explain RAG
Prompt Templates

PromptTemplate separates prompt logic from application logic.

Example:

{
    "question": "Explain RAG"
}

is injected into:

{question}
Chains

A Chain is a sequence of components where the output of one component becomes the input of the next component.

Example:

Input

 |

PromptTemplate

 |

ChatModel

 |

OutputParser

 |

Answer

Implemented Chain:

chain = (
    prompt
    |
    model
    |
    output_parser
)
Day 1 Result

Implemented:

First LangChain LLM call
ChatModel usage
SystemMessage / HumanMessage
PromptTemplate
First LCEL Chain