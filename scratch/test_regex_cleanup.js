const raw = `# 📚 Executive Legal Audit Dossier ## 1. ⚖️ Executive Legal Risk Overview & Overall Rating The legal audit of the proposed plan to open retail branches in the selected districts of Assam reveals a **Moderate Risk** profile with a score of 65/100. The primary areas of concern include statutory compliance and the specificity of legal agreements. While the regulatory compliance assessment indicates general alignment with key statutes, attention is required for confidentiality and IP protection measures. ## 2. 🔍 Clause-by-Clause Audit & Redline Recommendations | Clause Name | Risk Level | Problem | Recommended Redline | |---------------------------|------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------| | Statutory Compliance | HIGH | The contract lacks specific details on statutory compliance requirements for opening retail branches in Assam, which could lead to legal and regulatory issues. | Include a detailed section outlining the specific statutory compliance requirements, including permits, licenses, and local regulations necessary for operating retail branches in Assam. | | Legal Agreements Drafting | MEDIUM | The clause is vague about the nature and scope of the legal agreements to be drafted, which could result in incomplete or inadequate legal documentation. | Specify the types of legal agreements required (e.g., lease agreements, employment contracts, supplier agreements) and outline the key terms and conditions that must be included in each. |`;

function cleanMarkdown(text) {
  let cleaned = text;
  // 0. Strip leading whitespace before markdown headers (e.g. " ## Header" -> "## Header")
  cleaned = cleaned.replace(/^[ \t]+(#{1,4}\s+)/gm, '$1');
  cleaned = cleaned.replace(/\n[ \t]+(#{1,4}\s+)/g, '\n\n$1');

  // 1. Fix jammed Markdown headings (e.g. "Dossier ## 1. " -> "Dossier\n\n## 1. ")
  cleaned = cleaned.replace(/([^\n])\s*(#{1,4}\s+)/g, '$1\n\n$2');

  // 2. Fix start of table when jammed onto text: line starts with non-pipe text then has |
  cleaned = cleaned.replace(/^([^|\n]+)[ \t]*(\|.+)$/gm, '$1\n\n$2');

  // 3. Fix jammed table rows (when a row ends with | and next row starts with |)
  cleaned = cleaned.replace(/\|\s*\|/g, '|\n|');

  // 4. Fix jammed list items
  cleaned = cleaned.replace(/([^\n])\s*(\n?-\s+\*\*)/g, '$1\n\n- **');
  cleaned = cleaned.replace(/([^\n])\s*(\n?-\s+)/g, '$1\n- ');
  return cleaned;
}

const res = cleanMarkdown(raw);
console.log("CLEANED RESULT:\n" + res);
