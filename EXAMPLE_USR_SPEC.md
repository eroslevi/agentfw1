# Example: Document Analysis System (USR_SPEC)

This is an example User System Specification (USR_SPEC) showing how to define a multi-agentic system using the framework.

## Project Title
Intelligent Document Analysis System

## Project Description
A multi-agentic system that analyzes documents from various sources, extracts key information, identifies patterns, and generates intelligent summaries and recommendations. The system should process documents concurrently, maintain consistency across analyses, and provide audit trails for all decisions.

## Primary Goals

1. **Automated Document Processing**: Automatically process documents in multiple formats (PDF, DOCX, TXT) without manual intervention
2. **Information Extraction**: Extract structured data from unstructured document content with high accuracy (>95%)
3. **Pattern Recognition**: Identify patterns, anomalies, and relationships within document content
4. **Intelligent Summarization**: Generate concise, contextual summaries highlighting the most important information
5. **Recommendation Generation**: Based on document analysis, provide actionable recommendations to users

## Key Requirements

- Support multiple document formats: PDF, DOCX, TXT, CSV
- Process up to 100 concurrent document requests
- Complete analysis within 30 seconds per document
- Maintain 99.9% system availability
- Support documents up to 50MB in size
- Provide detailed audit logs for compliance
- Return structured JSON output for all analyses
- Support user feedback loop for continuous improvement
- Handle multiple languages (English, Spanish, French initially)

## Input Data / Context

The system receives:

1. **Documents**: Raw document files in supported formats (PDF, DOCX, TXT, CSV)
2. **User Preferences**: Optional user-specified analysis focus areas (e.g., financial data, technical details)
3. **Context Information**: Domain or industry context for specialized analysis
4. **Processing Options**: User-configurable analysis depth (quick scan, standard, comprehensive)

Example input:
```json
{
  "document_path": "/path/to/document.pdf",
  "document_type": "financial_report",
  "user_preferences": {
    "focus_areas": ["revenue", "profitability", "risks"],
    "analysis_depth": "comprehensive"
  },
  "context": "Q3 2024 Financial Analysis"
}
```

## Expected Output

The system produces:

1. **Analysis Results**: Structured data including:
   - Extracted entities (people, organizations, dates, financial figures)
   - Key themes and topics
   - Sentiment analysis
   - Risk factors identified
   - Recommendations

2. **Summary**: Executive summary (2-3 paragraphs)

3. **Metadata**: 
   - Processing timestamp
   - Document length
   - Languages detected
   - Confidence scores

4. **Audit Trail**: Complete record of:
   - Processing steps performed
   - Agents involved
   - Tools used
   - Time spent on each step

Example output:
```json
{
  "document_id": "doc_12345",
  "status": "completed",
  "processing_time_ms": 8500,
  "summary": "The Q3 2024 financial report shows...",
  "extracted_data": {
    "revenue": "$5.2M",
    "profit_margin": "12.3%",
    "entities": ["John Doe", "Acme Corp", "2024-09-30"]
  },
  "recommendations": [
    "Consider increasing marketing budget",
    "Review vendor contracts for cost reduction"
  ],
  "confidence_score": 0.94,
  "audit_trail": [...]
}
```

## Constraints and Limitations

1. **Performance**: Must complete analysis within 30 seconds per document
2. **Accuracy**: Must maintain >95% accuracy on entity extraction
3. **Scale**: Must handle 100 concurrent requests without degradation
4. **Storage**: Generated analyses must be stored for audit purposes (30-day minimum retention)
5. **Privacy**: Must comply with data privacy regulations (GDPR, CCPA)
6. **Language**: Initially support English, Spanish, French (extensible to other languages)
7. **Security**: All API communications must use TLS 1.2+, API authentication required
8. **Availability**: Target 99.9% uptime SLA

## Success Criteria

### Functional Success
- ✓ System correctly processes all supported document formats
- ✓ Extracted data matches manual review with >95% accuracy
- ✓ System generates meaningful summaries for all document types
- ✓ Recommendations are actionable and relevant

### Performance Success
- ✓ 95th percentile response time < 25 seconds
- ✓ System handles 100 concurrent requests with <5% error rate
- ✓ Document processing throughput > 200 documents/hour

### Quality Success
- ✓ User satisfaction score > 4/5 in user testing
- ✓ Generated summaries rated "good" or "excellent" by domain experts
- ✓ Zero critical security vulnerabilities found in security audit
- ✓ Audit log completeness 100% for all operations

### Operational Success
- ✓ System uptime > 99.9% measured over 30-day period
- ✓ All system errors logged with sufficient context for debugging
- ✓ Automated alerts for anomalies or performance degradation
- ✓ Successful deployment to production with zero data loss

---

## How to Use This Example

1. Use this as a template for your own USR_SPEC
2. Replace project details with your system requirements
3. Be as specific as possible about inputs, outputs, and constraints
4. Define clear success criteria that can be measured
5. Provide realistic constraints and limitations
6. Include concrete examples of input and output data

## Next Steps

Once you've created your USR_SPEC:

1. Run ARCH_PROMPT to generate architectural design
2. Review and refine the ARCH_SPEC with domain experts
3. Run TECH_PROMPT to get technical specifications
4. Use CODE_PROMPT to generate source code
5. Run TECH_SPEC_PROMPT to get test specifications
6. Use TEST_CODE_PROMPT to generate test suite
7. Execute CHK to validate and refine the system
