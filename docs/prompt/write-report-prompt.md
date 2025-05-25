
You are tasked with creating a detailed research report based on the CodeXRay process output for a given codebase. This report will provide insights into the codebase's structure, complexity, and potential areas for improvement.

First, you will be given a list of JSON files produced by the CodeXRay process. These files contain various metrics and analyses of the codebase. You should read and parse these files to extract the necessary information for your report.

<json_files_1>
/Users/kinglerbercy/Projects/mabos-workbench/agentdock-mabos-analysis.json,
</json_files_1>

<json_files_2>
/Users/kinglerbercy/Projects/mabos-workbench/dify-mabos-analysis.json,
</json_files_2>

<json_files_3>
/Users/kinglerbercy/Projects/mabos-workbench/kestra-kb-analysis.json
</json_files_3>

<json_files_4>
/Users/kinglerbercy/Projects/mabos-workbench/mabos-standalone-analysis.json
</json_files_4>

Your report should be comprehensive and well-structured. Use the following outline for your report in markdow format:

1. Executive Summary
2. Introduction
   2.1 Purpose of the Analysis
   2.2 Codebase Overview
3. Code Metrics
   3.1 Size and Complexity
   3.2 Code Duplication
   3.3 Maintainability Index
4. Architecture Analysis
   4.1 Module Dependencies
   4.2 Coupling and Cohesion
5. Code Quality
   5.1 Coding Standards Compliance
   5.2 Potential Bug Patterns
6. Performance Analysis
   6.1 Resource Usage
   6.2 Bottlenecks and Optimization Opportunities
7. Security Analysis
   7.1 Vulnerability Assessment
   7.2 Security Best Practices
8. Recommendations
   8.1 Short-term Improvements
   8.2 Long-term Refactoring Suggestions
9. Conclusion

For each section of the report:

1. Executive Summary: Provide a high-level overview of the key findings and recommendations.

2. Introduction: Explain the purpose of the CodeXRay analysis and give a brief overview of the codebase, including its primary function and technology stack.

3. Code Metrics: Analyze and present key metrics such as lines of code, cyclomatic complexity, and code duplication percentage. Use charts or tables where appropriate to visualize the data.

4. Architecture Analysis: Describe the overall architecture of the codebase, including module dependencies, coupling between components, and cohesion within modules.

5. Code Quality: Assess the adherence to coding standards and identify any recurring patterns that might indicate potential bugs or maintenance issues.

6. Performance Analysis: Evaluate the resource usage of the codebase and identify any performance bottlenecks or areas for optimization.

7. Security Analysis: Conduct a vulnerability assessment and evaluate the codebase's adherence to security best practices.

8. Recommendations: Based on your analysis, provide actionable recommendations for both short-term improvements and long-term refactoring efforts.

9. Conclusion: Summarize the overall health of the codebase and reiterate the most critical findings and recommendations.

Throughout the report, use clear and concise language. Support your findings with specific examples from the codebase where possible. Use Markdown formatting to structure your report, including headers, lists, code blocks, and emphasis where appropriate.

After completing your analysis and writing the report, save it as a Markdown file with the following naming convention:

<codebase_name>-codexray-report.md

Where <codebase_name> is:
{{CODEBASE_NAME}}

Your final output should only include the content of the report, formatted in Markdown. Do not include any meta-commentary about the report-writing process or these instructions.