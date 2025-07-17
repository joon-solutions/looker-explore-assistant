These are the nuances to the current lookml that you should consider when generating the looker url:
- For any input containing relative time expressions (e.g., 'this year,' 'last month,' 'next week,' 'today,' 'tomorrow')
    - If the data type of the fields is string, dynamically resolve these terms to their absolute dates or date ranges with the following format.
        - year: YYYY
        - week: YYYY/W + number , e.g. 2025/W01
        - month: YYYY/M + number , e.g. 2025/M01
        - quarter: YYYY/Q + number , e.g. 2025/Q1
    - If the data type of the fields is date and time, dynamically resolve these terms to Looker filter expressions for relative dates (based on the section <looker_documentation> below)