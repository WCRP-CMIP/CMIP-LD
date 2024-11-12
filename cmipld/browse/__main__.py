from .__init__ import * 

def main():
    """CLI entry point for the JSON-LD processor."""
    parser = argparse.ArgumentParser(description='Process JSON-LD documents and extract dependencies')
    parser.add_argument('url', help='URL of the JSON-LD document to process')
    parser.add_argument('--deps','-d', action='store_true', help='Extract dependencies')
    parser.add_argument('--relative', action='store_true', help='Use relative URLs for dependencies')
    parser.add_argument('--no-compact', '-nc', action='store_true', help='Do not compact the document')
    parser.add_argument('--expand-ctx','-ctx', action='store_false', help='Do not expand context')
    parser.add_argument('--no-expand-links', '-nl', action='store_true', help='Do not expand linked documents')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--no-interactive', '-n',action='store_false',  help='Interactive Playground')
    # parser.add_argument('--no-compact', action='store_true', help='Do not compact the document')
    # data mode for jless 
    
    
    args = parser.parse_args()
    processor = JsonLdProcessor()
    
    
    if 'https://' not in args.url and re.match(matches, args.url):
                for k,v in mapping.items():
                    if k in args.url:
                        args.url = args.url.replace(k,v)
                        print(f"Resolving: {k}")
                        break
    
    print(args.url)
    
    try:
        if args.deps:
            
            # Extract dependencies  
            deps = processor.extract_dependencies(args.url, args.relative)
            result = sorted(list(deps))
        else:
            # Process document
            result = processor.expand_document(
                args.url,
                compact=not args.no_compact,
                expand_ctx=not args.expand_ctx,
                expand_links=not args.no_expand_links
            )
        
        # Output results
        
        if args.output:
            output = json.dumps(result, indent=2)
            with open(args.output, 'w') as f:
                f.write(output)
                
        if args.no_interactive:
            open_jless_with_memory(result)
        else:
            print(output)
            
    except Exception as e:
        print(f"Error processing document: {str(e)}", file=sys.stderr)
        sys.exit(1)


main()
