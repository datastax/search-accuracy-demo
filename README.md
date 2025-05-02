# Search Accuracy Demo with Langflow

This repository contains supplementary items for Hybrid Search in Langflow with DataStax Astra DB. More information can be found in [our blog](https://www.datastax.com/blog/hybrid-search-in-langflow).

## Contents

1. `Hybrid Search RAG - Accuracy Week.json` - **REQUIRED to use the flow** - This Langflow flow can be imported directly and used. It contains a **read-only** access token for Astra DB, so you can get started quickly and easily.
2. `ingest_squad_astra.py` - **OPTIONAL if you'd like to ingest your own collection** - This contains Python code which will allow you to create your own Astra DB Collections that allow you to reproduce the results of this demo in your own database.

## Instructions

1. Download the `Hybrid Search RAG - Accuracy Week.json` flow
2. Start your Langflow instance (instructions [here](https://www.langflow.org/))
3. Create a new blank flow
4. From the top menu, choose Import
5. Choose the file from step 1
6. Add your OpenAI keys to the two OpenAI components in the flow
7. Execute the flow by clicking `Playground` in the top right
