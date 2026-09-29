import sys
import json
from client import LexicalMetricsCalculator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-rouge-bleu-lexical-overlap-metrics-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_overlap_metrics",
                        "description": "Calculate BLEU and ROUGE-L scores between reference and hypothesis text",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "reference": {"type": "string"},
                                "hypothesis": {"type": "string"}
                            },
                            "required": ["reference", "hypothesis"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        args = params.get("arguments", {})
        r = args.get("reference", "")
        h = args.get("hypothesis", "")
        bleu = LexicalMetricsCalculator.calculate_bleu(r, h)
        rouge = LexicalMetricsCalculator.calculate_rouge_l(r, h)
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"bleu": bleu, "rouge_l": rouge})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
