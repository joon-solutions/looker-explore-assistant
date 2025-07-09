# Looker Filter Expressions

Filter expressions are an advanced way to filter Looker queries, and this page describes how to write them. In the Explore section of Looker you can use them by adding a filter and choosing the matches (advanced) option. They are also used in LookML for elements that take a filter parameter.

Please note the type of filter expression you can use depends on the type (ie. string, date and time, boolean, number) of field you are filtering on. Please ensure you are checking the field type when applying filter expressions. 
Filters are not always necessary to get results, do not apply filters if they are not needed.

## String

Matches in string filters depend on the case_sensitive setting in your model file, and on whether your dialect supports case-sensitivity. For example, if case_sensitive is enabled in your model, the expression FOO% will not match the word "food". If case_sensitive isn't enabled, or if your dialect doesn't support case-sensitivity, the expression FOO% will match the word "food".

| Example   | Description   |
|-----------|-------------------------------------------------------------------------------|
| FOO       | is equal to "FOO", exactly |
| FOO,BAR   | is equal to either "FOO" or "BAR", exactly  |
| %FOO%     | contains "FOO", matches "buffoon" and "fast |
| FOO%      | starts with "FOO", matches "foolish" and "food" but not "buffoon" or "fast food"   |
| %FOO      | ends with "FOO", matches "buffoo" and "fast foo" but not "buffoon" or "fast food"   |
| F%OD      | starts with an "F" and ends with "OD", matches "fast food"                                                                                   |
| EMPTY     | string is empty (has zero characters) or is null (no value)  |
| NULL      | value is null (when it is used as part of a LookML filter expression, place NULL in quotes, as shown on the filters documentation page)       |
| -FOO      | is not equal to "FOO" (is any value except "FOO"), matches "pizza", "trash", "fun" but not "foo"  |
| -FOO,-BAR | is not equal to either "FOO" or "BAR", matches any value except "FOO" and "BAR" |
| -%FOO%    | doesn't contain "FOO", does not match "buffoon" or "fast food"      |
| -FOO%     | doesn't start with "FOO", does not match "foolish" or "food"   |
| -%FOO     | doesn't end with "FOO", does not match "buffoo" or "fast foo"       |
| -EMPTY    | string is not empty (has at least one character)  |
| -NULL     | value of column is not null (when it is used as part of a LookML filter expression, place -NULL in quotes, as shown on the filters documentation page) |
| FOO%,BAR  | starts with "FOO" or is "BAR" exactly, matches "food" and matches "bar" but not "barfood"    |
| FOO%,-FOOD| starts with "FOO" but is not "FOOD"  |
| _UF       | has any single character followed by "UF", matches "buffoon"    |

## Date and Time

Looker date filtering allows for English phrases to be used instead of SQL date functions. Use this if the field type starts with date_. It might be date_date, date_time, date_week, date_month, date_quarter, or date_year.

For the following examples:

* {n} is an integer.
* {interval} is a time increment such as hours, days, weeks, or months. The phrasing you use determines whether the {interval} will include partial time periods or only complete time periods. For example, the expression 3 days includes the current, partial day as well as the prior two days. The expression 3 days ago for 3 days includes the previous three complete days and excludes the current, partial day. See the Relative Dates section for more information.
* {time} can specify a time formatted as either YYYY-MM-DD HH:MM:SS or YYYY/MM/DD HH:MM:SS, or a date formatted as either YYYY-MM-DD or YYYY/MM/DD. When using the form YYYY-MM-DD, be sure to include both digits for the month and day, for example, 2016-01. Truncating a month or day to a single digit is interpreted as an offset, not a date. For example, 2016-1 is interpreted as 2016 minus one year, or 2015.

These are all the possible combinations of date filters:

| Combination                                         | Example                                            | Notes                                                        |
|-----------------------------------------------------|----------------------------------------------------|--------------------------------------------------------------|
| this {interval}                                     | this month                                         | You can use this week, this month, this quarter, or this year. Note that this day isn't supported. If you want to get data from the current day, you can use today.    |
| {n} {interval}                                      | 3 days                                             | You can use a number combined with days, weeks, months, quarters or years. This will return the last number of days, weeks, months, quarters or years you specify in the combination. For example the last 6 months or last 30 days. This is a very common filter. |
| {n} {interval} ago                                  | 3 days ago                                         | You can use a number combined with days, weeks, months, quarters or years ago. This will return the day you specify in the combination. 3 days ago will return the date 3 days prior to the current date. For example 3 days ago will not include the days between 3 days ago and today. Do not confuse this with the {n} interval filter.  |
| {n} {interval} ago for {n} {interval}               | 3 months ago for 2 days                            | You can use a number combined with days, weeks, months, quarters or years ago for the duration of a number you and interval you specify. This will return date range you specify in the combination. 3 months ago for 2 days will return the date for a range of 2 days 3 months prior to the current date.    |
| before {n} {interval} ago                           | before 3 days ago                                  | You can use this combination to specify a number combined with days, weeks, months, quarters or years in the desired range before ending the date range. Before 3 days ago will return all dates before 3 days of the current date.    |
| before {time}                                       | before 2018-01-01 12:00:00                         | Before is not inclusive of the time you specify. The expression before 2018-01-01 will return data from all dates before 2018-01-01, but it won't return data from 2018-01-01. |
| after {time}                                        | after 2018-10-05                                   | After is inclusive of the time you specify. So, the expression after 2018-10-05 will return data from 2018-10-05 and all dates later than 2018-10-05.  |
| {time} to {time}                                    | 2018-05-18 12:00:00 to 2018-05-18 14:00:00         | The initial time value is inclusive but the latter time value is not. So the expression 2018-05-18 12:00:00 to 2018-05-18 14:00:00 will return data with the time "2018-05-18 12:00:00" through "2018-05-18 13:59:59". |
| this {interval} to {interval}                       | this year to second                                |    The beginning of each interval is used. For example, the expression this year to second returns data from the beginning of the year the query is run through to the beginning of the second the query is run. this week to day returns data from the beginning of the week the query is run through to the beginning of the day the query is run.   |
| {time} for {n} {interval}                           | 2018-01-01 12:00:00 for 3 days                     | The initial time value is inclusive but the latter number and interval values are not. So the expression 2018-05-18 12:00:00 for 3 days will return data with the time "2018-01-01 12:00:00" through "2018-01-04 12:00:00".    |
| today                                               | today                                              | Returns todays date    |
| yesterday                                           | yesterday                                          | Returns yesterdays date    |
| tomorrow                                            | tomorrow                                           | Returns tomorrows date |
| {day of week}                                       | Monday                                             | Specifying a day of week with a Dimension Group Date field returns the most recent date that matches the specified day of week. For example, the expression Dimension Group Date matches (advanced) Monday returns the most recent Monday. You can also use {day of week} with the before and after keywords in this context. For example, the expression Dimension Group Date matches (advanced) after Monday returns the most recent Monday and everything after the most recent Monday. The expression Dimension Group Date matches (advanced) before Monday returns every day before the most recent Monday, but it doesn't return the most recent Monday. Specifying a day of the week with a Dimension Group Day of Week field returns every day that matches the specified day of week. So the expression Dimension Group Day of Week matches (advanced) Monday returns every Monday.   |
| next {week, month, quarter, fiscal quarter, year, fiscal year} | next week                               | The next keyword is unique in that it requires one of the intervals listed previously and won't work with other intervals. |
| {n} {interval} from now                            | 3 days from now                                     | You can use a number combined with days, weeks, months, quarters or years from now. This will return a future date the number of days, weeks, months, quarters or years you specify in the combination.    |
| {n} {interval} from now for {n} {interval}         | 3 days from now for 2 weeks                         | You can use a number combined with days, weeks, months, quarters or years from now for the duration of a number you and interval you specify. This will return a date range in the future you specify in the combination. 3 days ago for 2 weeks will return the dates for a range of 3 days 2 weeks ahead of the current date.    |


Date filters can also be combined together:
* To get OR logic: Type multiple conditions into the same filter, separated by commas. For example, today, 7 days ago means "today or 7 days ago".
* To get AND logic: Type your conditions, one by one, into multiple date or time filters. For example, you could put after 2014-01-01 into a Created Date filter, then put before 2 days ago into a Created Time filter. This would mean "January 1st, 2014 and after, and before 2 days ago".

### Absolute Dates

Absolute date filters use the specific date values to generate query results. These are useful when creating queries for specific date ranges.

| Example                   | Description                                                                                                                  |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------|
| 2018/05/29                | sometime on 2018/05/29                                                                                                        |
| 2018/05/10 for 3 days     | from 2018/05/10 00:00:00 through 2018/05/12 23:59:59                                                                          |
| after 2018/05/10          | 2018/05/10 00:00:00 and after                                                                                                |
| before 2018/05/10         | before 2018/05/10 00:00:00                                                                                                   |
| 2018/05                   | within the entire month of 2018/05                                                                                           |
| 2018/05 for 2 months      | within the entire months of 2018/05 and 2018/06                                                                              |
| 2018/05/10 05:00 for 5 hours | from 2018/05/10 05:00:00 through 2018/05/10 09:59:59                                                                      |
| 2018/05/10 for 5 months   | from 2018/05/10 00:00:00 through 2018/10/09 23:59:59                                                                         |
| 2018                      | entire year of 2018 (2018/01/01 00:00:00 through 2018/12/31 23:59:59)                                                        |
| FY2018                    | entire fiscal year starting in 2018 (if your Looker developers have specified that your fiscal year starts in April then this is 2018/04/01 00:00 through 2019/03/31 23:59) |
| FY2018-Q1                 | first quarter of the fiscal year starting in 2018 (if your Looker developers have specified that your fiscal year starts in April then this is 2018/04/01 00:00:00 through 2018/06/30 23:59:59) |


### Relative Dates

Relative date filters allow you to create queries with rolling date values relative to the current date. These are useful when creating queries that update each time you run the query.

For all of the following examples, assume today is Friday, 2018/05/18 18:30:02. In Looker, weeks start on Monday unless you change that setting with week_start_day.

Relative date filters allow you to create queries with rolling date values relative to the current date. These are useful when creating queries that update each time you run the query.

For all of the following examples, assume today is Friday, 2018/05/18 18:30:02. In Looker, weeks start on Monday unless you change that setting with `week_start_day`.

#### Seconds
| Example                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| 1 second                     | the current second (2018/05/18 18:30:02)                 |
| 60 seconds                   | 60 seconds ago for 60 seconds (2018/05/18 18:29:02 through 2018/05/18 18:30:01) |
| 60 seconds ago for 1 second  | 60 seconds ago for 1 second (2018/05/18 18:29:02)        |

#### Minutes
| Example                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| 1 minute                     | the current minute (2018/05/18 18:30:00 through 18:30:59) |
| 60 minutes                   | 60 minutes ago for 60 minutes (2018/05/18 17:31:00 through 2018/05/18 18:30:59) |
| 60 minutes ago for 1 minute  | 60 minutes ago for 1 minute (2018/05/18 17:30:00 through 2018/05/18 17:30:59) |

#### Hours
| Example                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| 1 hour                       | the current hour (2018/05/18 18:00 through 2018/05/18 18:59) |
| 24 hours                     | the same hour of day that was 24 hours ago for 24 hours (2018/05/17 19:00 through 2018/05/18 18:59) |
| 24 hours ago for 1 hour      | the same hour of day that was 24 hours ago for 1 hour (2018/05/17 18:00 until 2018/05/17 18:59) |

#### Days
| Example                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| today                        | the current day (2018/05/18 00:00 through 2018/05/18 23:59) |
| 2 days                       | all of yesterday and today (2018/05/17 00:00 through 2018/05/18 23:59) |
| 1 day ago                    | just yesterday (2018/05/17 00:00 until 2018/05/17 23:59)  |
| 7 days ago for 7 days        | the last complete 7 days (2018/05/11 00:00 until 2018/05/17 23:59) |
| today for 7 days             | the current day, starting at midnight, for 7 days into the future (2018/05/18 00:00 until 2018/05/24 23:59) |
| last 3 days                  | 2 days ago through the end of the current day (2018/05/16 00:00 until 2018/05/18 23:59) |
| 7 days from now              | 7 days in the future (2018/05/18 00:00 until 2018/05/25 23:59) |

#### Weeks
| Example                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| 1 week                       | top of the current week going forward (2018/05/14 00:00 through 2018/05/20 23:59) |
| this week                    | top of the current week going forward (2018/05/14 00:00 through 2018/05/20 23:59) |
| before this week             | anytime until the top of this week (before 2018/05/14 00:00) |
| after this week              | anytime after the top of this week (2018/05/14 00:00 and later) |
| next week                    | the following Monday going forward 1 week (2018/05/21 00:00 through 2018/05/27 23:59) |
| 2 weeks                      | a week ago Monday going forward (2018/05/07 00:00 through 2018/05/20 23:59) |
| last week                    | synonym for "1 week ago"                                 |
| 1 week ago                   | a week ago Monday going forward 1 week (2018/05/07 00:00 through 2018/05/13 23:59) |

#### Months
| Example                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| 1 month                      | the current month (2018/05/01 00:00 through 2018/05/31 23:59) |
| this month                   | synonym for "0 months ago" (2018/05/01 00:00 through 2018/05/31 23:59) |
| 2 months                     | the past two months (2018/04/01 00:00 through 2018/05/31 23:59) |
| last month                   | all of 2018/04                                            |
| 2 months ago                 | all of 2018/03                                            |
| before 2 months ago          | all time before 2018/03/01                                |
| next month                   | all of 2018/06                                            |
| 2 months from now            | all of 2018/07                                            |
| 6 months from now for 3 months | 2018/11 through 2019/01                                  |

* note for relative dates, the last 3 days is much more common than 3 days ago. The last 2 years is much more common that 2 years ago. 

#### Years

| Example             | Description                                                                                          |
|---------------------|------------------------------------------------------------------------------------------------------|
| 1 year              | all of the current year (2018/01/01 00:00 through 2018/12/31 23:59)                                  |
| this year           | all of the current year (2018/01/01 00:00 through 2018/12/31 23:59)                                  |
| next year           | all of the following year (2019/01/01 00:00 through 2019/12/31 23:59)                                |
| 2 years             | the past two years (2017/01/01 00:00 through 2018/12/31 23:59)                                       |
| last year           | all of 2017                                                                                          |
| 2 years ago         | all of 2016                                                                                          |
| before 2 years ago  | all time before 2016/01/01 (does not include any days between 2016/01/01 and 2016/05/18)             |

## Boolean

Filtering on true or false type values in Looker requires you to know what type of true or false value you're interacting with. Use this if the field type is a yesno or boolean.

### Examples

| Example      | Description                                                                                                           |
|--------------|-----------------------------------------------------------------------------------------------------------------------|
| yes or Yes   | field evaluates to true                                                                                               |
|              | **Looker developers:** for `type: yesno` dimensions use lowercase, for filters parameters (like those used in a measure or used in an `always_filter`) use uppercase |
| no or No     | field evaluates to false                                                                                              |
|              | **Looker developers:** for `type: yesno` dimensions use lowercase, for filters parameters (like those used in a measure or used in an `always_filter`) use uppercase |
| TRUE         | field contains true (for fields that contain Boolean database values)                                                 |
| FALSE        | field contains false (for fields that contain Boolean database values)                                                |

## Numbers

Filters on numbers support both natural language expressions (for example, `3 to 10`) and relational operators (for example, `>20`). Looker supports the `OR` operator to express multiple filter ranges (for example, `3 to 10 OR 30 to 100`). The `AND` operator can be used to express numeric ranges with relational operators (for example, `>=3 AND <=10`) to specify a range. Filters on numbers can also use algebraic interval notation to filter numeric fields.

**Note:** The syntax for numeric filter expressions using `NOT` may not be intuitive. If the first filter condition contains a `NOT`, and no other filter conditions contain a `NOT`, then all of the filter conditions will be negated. See the following examples for more information.

#### Examples

| Example                      | Description                                                                                              |
|------------------------------|----------------------------------------------------------------------------------------------------------|
| 5                            | is exactly 5                                                                                            |
| NOT 5                        | is any value but exactly 5                                                                               |
| <>5                          | is any value but exactly 5                                                                               |
| !=5                          | is any value but exactly 5                                                                               |
| 1, 3, 5, 7                   | is one of the values 1, 3, 5, or 7, exactly                                                              |
| NOT 66, 99, 4                | is not one of the values 66, 99, or 4, exactly                                                           |
| >1 AND <100, NOT 2           | is greater than 1 and less than 100, is not 2                                                            |
| NOT >1, 2, <100              | is less than or equal to 1, is not 2, and is greater than or equal to 100 (Looker recognizes that this is an impossible condition, and will instead write the SQL `IS NULL`) |
| 5, NOT 6, NOT 7              | is 5, is not 6 or 7                                                                                      |
| 5.5 to 10                    | is 5.5 or greater but also 10 or less                                                                    |
| >=5.5 AND <=10               | is 5.5 or greater but also 10 or less                                                                    |
| NOT 3 to 80.44               | is less than 3 or greater than 80.44                                                                     |
| <3 OR >80.44                 | is less than 3 or greater than 80.44                                                                     |
| 1 to                         | is 1 or greater                                                                                          |
| >=1                          | is 1 or greater                                                                                          |
| to 10                        | is 10 or less                                                                                            |
| <=10                         | is 10 or less                                                                                            |
| >10 AND <=20 OR 90           | is greater than 10 and less than or equal to 20, or is 90 exactly                                        |
| >=50 AND <=100 OR >=500 AND <=1000 | is between 50 and 100, inclusive, or between 500 and 1000, inclusive                                      |
| NULL                         | has no data in it (when it is used as part of a LookML filter expression, place `NULL` in quotes, as shown on the filters documentation page) |
| NOT NULL                     | has some data in it (when it is used as part of a LookML filter expression, place `NOT NULL` in quotes, as shown on the filters documentation page) |
| (1, 7)                       | interpreted as 1 < x < 7 where the endpoints aren't included. While this notation resembles an ordered pair, in this context it refers to the interval upon which you are working. |
| [5, 90]                      | interpreted as 5 <= x <= 90 where the endpoints are included                                             |
| (12, 20]                     | interpreted as 12 < x <= 20 where 12 is not included, but 20 is included                                 |
| [12, 20)                     | interpreted as 12 <= x < 20 where 12 is included, but 20 is not included                                 |
| (500, inf)                   | interpreted as x > 500 where 500 is not included and infinity is always expressed as being "open" (not included). `inf` may be omitted and (500, inf) may be written as (500,) |
| (-inf, 10]                   | interpreted as x <= 10 where 10 is included and infinity is always expressed as being "open" (not included). `inf` may be omitted and (-inf, 10] may be written as (,10] |
| [0,9],[20,29]                | the numbers between 0 and 9 inclusive or 20 to 29 inclusive                                              |
| [0,10],20                    | 0 to 10 inclusive or 20                                                                                  |
| NOT (3,12)                   | interpreted as x < 3 and x > 12
                                                                          |
## Intervals

Interval options
The intervals parameter tells the dimension group which interval units it should use to measure the time difference between the sql_start time and the sql_end time. The intervals parameter is supported only for dimension groups of type: duration.

If intervals is not included, the dimension group will include all possible intervals.

The options for the intervals parameter are:

Interval |  Description | Example Output
|--------|-------------------------------------------------------------|--------------------|
day	     |  Calculates a time difference in days.                      |	9 days
hour	 |  Calculates a time difference in hours.                     |	171 hours
minute	 |  Calculates a time difference in minutes.                   |	10305 minutes
month	 |  Calculates a time difference in months.	                   |    3 months
quarter	 |  Calculates a time difference in quarters of the year.	   |    2 quarters
second	 |  Calculates a time difference in seconds.	               |    606770 seconds
week	 |  Calculates a time difference in weeks.	                   |    6 weeks
year	 |  Calculates a time difference in years.	                   |    2 years

## Timeframes

Timeframe options
The timeframes parameter is supported only for dimension groups of type: time. For dimension groups of type: duration, use the intervals parameter instead.

The timeframes parameter tells the dimension group which dimensions it should produce and includes the following options:

Special timeframes
Time timeframes
Date timeframes
Week timeframes
Month timeframes
Quarter timeframes
Year timeframes
hourX timeframes
minuteX timeframes
millisecondX timeframes

Special timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
raw	      | The raw value from your database, without casting or time zone conversion. raw is accessible only within LookML and won't show up on the Explore page. The raw timeframe returns a timestamp, unlike most other timeframes that return a formatted string. It is primarily used for performing date operations on a field. | 2014-09-03 17:15:00 +0000
yesno	  | A yesno dimension, returning "Yes" if the datetime has a value, otherwise "No". Unlike other timeframes, when you refer to a yesno timeframe dimension from another field, don't include the timeframe in the reference. For example, to refer to a yesno timeframe in the dimension_group: created, use the syntax $ {created}, not $ {created_yesno}. | Yes

Time timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
time	     | Datetime of the underlying field (some SQL dialects show as much precision as your database contains, while others show only to the second)	| 2014-09-03 17:15:00
time_of_day  | Time of day | 17:15
hour	     | Datetime truncated to the nearest hour | 2014-09-03 17
hour_of_day  | Integer hour of day of the underlying field |	17
hourX	     | Splits each day into intervals with the specified number of hours. |	See Using hourX.
minute	     | Datetime truncated to the nearest minute | 2014-09-03 17:15
minuteX	     | Splits each hour into intervals with the specified number of minutes. | See Using minuteX.
second	     | Datetime truncated to the nearest second	| 2014-09-03 17:15:00
millisecond	 | Datetime truncated to the nearest millisecond (see the Dialect support for milliseconds and microseconds section on this page for information on dialect support). | 2014-09-03 17:15:00.000
millisecondX |	Splits each second into intervals with the specified number of milliseconds (see the Dialect support for milliseconds and microseconds section on this page for information on dialect support). | See Using millisecondX.
microsecond  |	Datetime truncated to the nearest microsecond (see the Dialect support for milliseconds and microseconds section on this page for information on dialect support). | 2014-09-03 17:15:00.000000

Date timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
date      | Date of the underlying field | 2017-09-03

Week timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
week	          | Date of the week starting on a Monday of the underlying datetime | 2017-09-01
day_of_week	      | Day of week alone | Wednesday
day_of_week_index |	Day of week index (0 = Monday, 6 = Sunday) | 2

Month timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
month	         | Year and month of the underlying datetime | 2014-09
month_num	     | Integer number of the month of the underlying datetime | 9
fiscal_month_num |	Integer number of the fiscal month of the underlying datetime | 6
month_name	     | Name of the month | September
day_of_month	 | Day of month | 3
To use the fiscal_month_num timeframes, the fiscal_month_offset parameter must be set in the model.

Quarter timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
quarter	               | Year and quarter of the underlying datetime | 2017-Q3
fiscal_quarter         | Fiscal year and quarter of the underlying datetime | 2017-Q3
quarter_of_year	       | Quarter of the year preceded by a "Q" | Q3
fiscal_quarter_of_year | Fiscal quarter of the year preceded by a "Q" | Q3
To use the fiscal_quarter and fiscal_quarter_of_year timeframes, the fiscal_month_offset parameter must be set in the model.

Year timeframes
Timeframe | Description | Example Output
|---------|-------------|-------------------------------------------------------------------|
year	     | Integer year of the underlying datetime | 2017
fiscal_year	 | Integer fiscal year of the underlying datetime | FY2017
day_of_year	 | Day of year | 143
week_of_year |	Week of the year as a number | 17
To use the fiscal_year timeframe, the fiscal_month_offset parameter must be set in the model.


Using hourX
In hourX the X is replaced with 2, 3, 4, 6, 8, or 12.

This will split up each day into intervals with the specified number of hours. For example, hour6 will split each day into 6 hour segments, which will appear as follows:

2014-09-01 00:00:00
2014-09-01 06:00:00
2014-09-01 12:00:00
2014-09-01 18:00:00
To give an example, a row with a time of 2014-09-01 08:03:17 would have a hour6 of 2014-09-01 06:00:00.


Using minuteX
In minuteX the X is replaced with 2, 3, 4, 5, 6, 10, 12, 15, 20, or 30.

This will split up each hour into intervals with the specified number of minutes. For example, minute15 will split each hour into 15 minute segments, which will appear as follows:

2014-09-01 01:00:00
2014-09-01 01:15:00
2014-09-01 01:30:00
2014-09-01 01:45:00
To give an example, a row with a time of 2014-09-01 01:17:35 would have a minute15 of 2014-09-01 01:15:00.


Using millisecondX
In millisecondX the X is replaced with 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, or 500.

This will split up each second into intervals with the specified number of milliseconds. For example, millisecond250 will split each second into 250 millisecond segments, which will appear as follows:

2014-09-01 01:00:00.000
2014-09-01 01:00:00.250
2014-09-01 01:00:00.500
2014-09-01 01:00:00.750
To give an example, a row with a time of 2014-09-01 01:00:00.333 would have a millisecond250 of 2014-09-01 01:00:00.250.
                                                                          |# Expanded URL generation

JSON Payload Fields:

fields: fields=view.field_1,view.field_2,view.count
 This parameter specifies the list of fields to be included in the results. In this example, the explore will return data for view.field_1, view.field_2, and the count of rows (view.count).

f[]: &f[view.filter_1_dimension]={{ value }} & &f[view.filter_2_on_date]=last+60+days
 This parameter defines filters for the explore. The f[] syntax is used to declare a filter on a specific dimension (view.filter_1_dimension and view.filter_2_on_date in this case). The {{ value }} placeholder indicates a dynamic value that can be passed through the URL. The second filter uses a Looker expression (last+60+days) to filter data for the past 60 days.

pivots: pivots=view.field_2 This parameter defines the dimension to pivot on. In this example, view.field_2 will be used to create a pivot table.

limit: limit=50 This parameter sets the maximum number of rows to be returned by the explore. The default limit is 5000, but here it's explicitly set to 50.

column_limit: column_limit=20 This parameter sets the maximum number of columns to be displayed in the pivot table. This parameter only has an effect when a pivot dimension is specified (as seen with pivots). The column_limit can be between 1 and 200. Dimensions, dimension table calculations, row total columns, and measure table calculations outside of pivots are not counted toward the column limit. Pivoted groups each count as one column toward the column limit.

total: total=true This parameter controls whether to display column totals in the explore results. Here, true indicates that column totals will be shown.

row_total: row_total=right This parameter controls whether to display row totals in the explore results. Here, right specifies that the row totals will be displayed on the right side. Only use row totals if the chart contains pivots.

sorts: sorts=view.field_1,view.count+desc This parameter defines the order in which the results should be sorted. The first field (view.field_1) is sorted by default in ascending order. The second sort (view.count+desc) sorts the results by view.count in descending order. The +desc syntax specifies descending order.

filter_config: The filter_config parameter contains detailed JSON objects that control the filtering aspects of the query. The filter_config represents the state of the filter UI on the explore page for a given query. When running a query via the Looker UI, this parameter takes precedence over "filters". 

Vis:  The vis parameter contains detailed JSON objects that control the visualization properties of the query. These properties are typically opaque and differ based on the type of visualization used. There is no specified set of allowed keys. The values can be any type supported by JSON. A "type" key with a string value is often present, and is used by Looker to determine which visualization to present. Visualizations ignore unknown vis_config properties.

Query_timezone: User's timezone, string value.

Subtotals: When using a table visualization and your data table contains at least two dimensions, you can apply subtotals. Subtotals are not available when you filter on a measure or when the Explore uses the sql_always_having parameter. List of fields to run the subtotals. The leftmost subtotal is always sorted. When you sort by multiple columns, subtotal columns are given precedence. Fields on which to run subtotals. 

# Pivot table reference

In Looker, pivots allow you to turn a selected dimension into several columns, which creates a matrix of your data similar to a pivot table in spreadsheet software. This is very useful for analyzing metrics by different groupings of your data, such as getting counts for category or label in your dataset.

When you pivot on a dimension, each unique possible value of that dimension becomes its own column header. Any measures are then repeated under each column header. 

Pivots make it much easier to compare a measure accross dimensions. It also shows you gaps in your data, where you don’t have any numeric values for a particular dimension field. In summary, pivots allow you to create and display a matrix of your data, similar to a pivot table in spreadsheet software. Specifically, pivots turn a selected dimension into several columns and are applied only to the visual display of your results.

With pivots, Looker allows you to regroup your data, so that you can easily compare results by different groupings and identify potential gaps, all while leaving your underlying data unaffected.

Whenever you have a question involving one dimension “by” another dimension, that’s a clue that a pivot might come in handy.

When two time dimensions are in a report and a pivot is required, always pivot by the least granular time dimension. 

|Example                                                                   | Pivoted Dimension                |
|--------------------------------------------------------------------------|----------------------------------|
| What were the hourly total sales by day in the past 3 days?              | Day                              |
| What were the daily total sales by week in the past 3 weeks?             | Week                             |
| What were the total sales by day each week in the past 2 weeks?          | Week                             |
| What were the total sales by day of week each week in the past 2 weeks?  | Week                             |
| What were the weekly total sales by month in the past 2 months?          | Month                            |
| What were the monthly total sales by quarter in the past 2 quarters?     | Quarter                          |
| What were the monthly total sales by quarter in the past 2 years?        | Year                             |
| What were the total sales by week of year each year in the past 2 years? | Year                             |
| What were the monthly total sales by year in the past 2 years?           | Year                             |
| What were the weekly total sales by quarter in the past 3 years?         | Quarter                          |

# Looker API JSON Fields

|application/JSON          |    Datatype            | Description
|--------------------------|------------------------|------------------------------------------------------------------------------------------
| can                      | Hash[boolean]          | Operations the current user is able to perform on this object
| id                       | string                 | Unique Id
| model                    | string                 | Model
| view                     | string                 | Explore Name
| fields                   | string[]               | Fields
| pivots                   | string[]               | Pivots
| fill_fields              | string[]               | Fill Fields
| filters                  | Hash[string]           | Filters will contain data pertaining to complex filters that do not contain "or" conditions. When "or" conditions are present, filter data will be found on the filter_expression property.
| filter_expression        | string                 | Filter Expression
| sorts                    | string[]               | Sorting for the query results. Use the format ["view.field", ...] to sort on fields in ascending order. Use the format ["view.field desc", ...] to sort on fields in descending order. Use ["__UNSORTED__"] (2 underscores before and after) to disable sorting entirely. Empty sorts [] will trigger a default sort.
| limit                    | string                 | Row limit. To download unlimited results, set the limit to -1 (negative one).
| column_limit             | string                 | Column Limit
| total                    | boolean                | Total
| row_total                | string                 | Raw Total
| subtotals                | string[]               | Fields on which to run subtotals
| vis_config               | Hash[any]              | Visualization configuration properties. These properties are typically opaque and differ based on the type of visualization used. There is no specified set of allowed keys. The values can be any type supported by JSON. A "type" key with a string value is often present, and is used by Looker to determine which visualization to present. Visualizations ignore unknown vis_config properties.
| filter_config            | Hash[any]              | The filter_config represents the state of the filter UI on the explore page for a given query. When running a query via the Looker UI, this parameter takes precedence over "filters". When creating a query or modifying an existing query, "filter_config" should be set to null. Setting it to any other value could cause unexpected filtering behavior. The format should be considered opaque.
| visible_ui_sections      | string                 | Visible UI Sections
| slug                     | string                 | Slug
| dynamic_fields           | string                 | Dynamic Fields
| client_id                | string                 | Client Id: used to generate shortened explore URLs. If set by client, must be a unique 22 character alphanumeric string. Otherwise one will be generated.
| share_url                | string                 | Share Url
| expanded_share_url       | string                 | Expanded Share Url
| url                      | string                 | Expanded Url
| query_timezone           | string                 | Query Timezone
| has_table_calculations   | boolean                | Has Table Calculations
                                                                          |
# Looker Visualization Config Documentation


## Customizing Visualizations Using the Chart Config Editor

You can use the Chart Config Editor to customize formatting options on Looker visualizations that use the HighCharts API. This includes most Cartesian charts, such as the column chart, bar chart, and line chart, among others.

### Prerequisites

To access the Chart Config Editor, you must have the `can_override_vis_config` permission.

### Customizing a Visualization

To customize a visualization with the Chart Config Editor, follow these steps:

1. **View or Edit a Visualization**: 
   - View a visualization in an Explore, or edit a visualization in a Look or dashboard.
   
2. **Open the Chart Config Editor**:
   - Open the Edit menu in the visualization.
   - Click the **Edit Chart Config** button in the Plot tab. Looker displays the Edit Chart Config dialog.

3. **Modify the JSON**:
   - The **Chart Config (Source)** pane contains the original JSON of your visualization and cannot be edited.
   - The **Chart Config (Override)** pane contains the JSON that should override the source JSON. When you first open the Edit Chart Config dialog, Looker populates the pane with some default JSON. You can start with this JSON or delete it and enter any valid HighCharts JSON.
   - Select the Chart Config (Override) section and enter valid HighCharts JSON. The new values will override any values in the Chart Config (Source) section.

4. **Format and Apply Changes**:
   - Click `<>` (Format code) to allow Looker to properly format your JSON.
   - Click **Preview** to test your changes.
   - Click **Apply** to apply your changes. The visualization will be displayed using the custom JSON values.

5. **Save the Visualization**:
   - Once you've customized your visualization, save it. If you viewed the visualization in an Explore, save the Explore. If you edited a Look or a dashboard, click Save.

### Caution

Do not edit the default visualization options after making changes in the Chart Config Editor. Editing the default visualization options may cause unexpected behavior, including blank visualizations. If you'd like to edit the default visualization options, first remove any changes you've made in the Chart Config Editor, then replace them later. Specifically, follow these steps:

1. Click the **Edit Chart Config** button in the Plot tab. Looker displays the Edit Chart Config dialog.
2. Copy the text in the Chart Config (Override) pane.
3. Click the **Clear Chart Overrides** button to delete all changes.
4. Click **Apply**.
5. Edit your visualization using the default visualization options.
6. Click the **Edit Chart Config** button in the Plot tab. Looker displays the Edit Chart Config dialog.
7. Enter some valid HighCharts JSON in the Chart Config (Override) pane. You can use the text that you copied in step 2 as a template, but be sure to test your changes using the Preview button to ensure there are no conflicts.
8. Click **Apply**.

### Conditional Formatting with Series Formatters

The Chart Config Editor accepts most valid HighCharts JSON. It also accepts the `series.formatters` attribute, which only exists in Looker. Each series can have multiple formatters to combine different style rules.

The `series.formatters` attribute accepts two attributes: `select` and `style`.

- Enter a logical expression in the `select` attribute to indicate which data values will be formatted.
- Enter some JSON into the `style` attribute to indicate how to format the data values.

For example, the following JSON will color each data value orange if it is greater than or equal to 380:

```json
{
  "series": [{
    "formatters": [{
      "select": "value >= 380",
      "style": {
        "color": "orange"
      }
    }]
  }]
}
```

#### The `select` Attribute

You can use the following values in a `select` expression:

- `value`: This variable returns the value of the series. For example, you could use `select: value > 0` to target all positive values, or `value = 100` to only match series with a value of 100.
- `max`: Use `select: max` to target the series value that has the maximum value.
- `min`: Use `select: min` to target the series value that has the minimum value.
- `percent_rank`: This variable targets the series value with a specified percentile. For example, you could use `select: percent_rank >= 0.9` to target series values in the ninetieth percentile.
- `name`: This variable returns the dimension value of the series. For example, if you had a report showing Sold, Canceled, and Returned orders, you could use `select: name = Sold` to target the series where the dimension value is Sold.
- `AND/OR`: Use `AND` and `OR` to combine multiple logical expressions.

#### The `style` Attribute

The `style` attribute can be used to apply styles that HighCharts supports. For example, you can color series values using `style.color`, color series borders using `style.borderColor`, and set series border width using `style.borderWidth`. For a more complete list of style options, see the Highcharts options for `series.column.data`.

For line visualizations, use `style.marker.fillColor` and `style.marker.lineColor` instead of `style.color`. For a more complete list of line style options, see the Highcharts options for `series.line.data.marker`.

### Examples

The following sections provide examples of some common use cases for the Chart Config Editor. For a complete list of the attributes that you can edit, see the [HighCharts API documentation](https://api.highcharts.com/highcharts/).

#### Change the Background Color and Axis Text Color

To change the background color of a visualization, use the `chart.backgroundColor` attribute.

Similarly, to change the text color of the axes in a visualization, use the following attributes:

- `xAxis.labels.style.color`
- `xAxis.title.style.color`
- `yAxis.labels.style.color`
- `yAxis.title.style.color`

The following HighCharts JSON changes the background color of the visualization to purple, and the text of the axis titles and labels to white.

```json
{
  "chart": {
    "backgroundColor": "purple"
  },
  "xAxis": {
    "labels": {
      "style": {
        "color": "white"
      }
    },
    "title": {
      "style": {
        "color": "white"
      }
    }
  },
  "yAxis": {
    "labels": {
      "style": {
        "color": "white"
      }
    },
    "title": {
      "style": {
        "color": "white"
      }
    }
  }
}
```

#### Customize Tooltip Color

To customize the color of the tooltip, use the following attributes:

- `tooltip.backgroundColor`
- `tooltip.style.color`

The following HighCharts JSON changes the background color of the tooltip to cyan, and changes the color of the tooltip text to black.

```json
{
  "tooltip": {
    "backgroundColor": "cyan",
    "style": {
      "color": "black"
    }
  }
}
```

#### Customize Tooltip Content and Styles

To customize the content of the tooltip, use the following attributes:

- `tooltip.format`
- `tooltip.shared`

The following HighCharts JSON changes the tooltip format such that the x-axis value appears at the top of the tooltip in larger font, followed by a list of all series values at that point.

This example uses the following HighCharts functions and variables:

- `{key}` is a variable that returns the x-axis value of the selected point. (in this example, the month and year).
- `{#each points}{/each}` is a function that repeats the enclosed code for each series in the chart.
- `{series.name}` is a variable that returns the name of the series.
- `{y:.2f}` is a variable that returns the y-axis value of the selected point, rounded to two decimal places.
- `{y}` is a variable that returns the y-axis value of the selected point.
- `{variable:.2f}` rounds `variable` to two decimal places. See the [Highcharts templating documentation](https://api.highcharts.com/highcharts/tooltip.formatter) for more examples of value formatting.

```json
{
  "tooltip": {
    "format": "<span style=\"font-size: 1.8em\">{key}</span><br/>{#each points}<span style=\"color:{color}; font-weight: bold;\">\\u25CF {series.name}: </span>{y:.2f}<br/>{/each}",
    "shared": true
  }
}
```

#### Add Chart Annotations and Captions

To add an annotation, use the `annotations` attribute. To add a caption to the chart, use the `caption` attribute.

To get the coordinates for a point, click **Inspect Point Metadata** at the top of the Edit Chart Config dialog. Then, hold the pointer over the data point that you'd like to annotate. Looker displays a point ID, which you can use in the `annotations.labels.point` attribute.

The following HighCharts JSON adds two annotations to the chart to explain a decrease in inventory items after certain periods of time. It also adds a caption to the bottom of the chart to explain the annotations in more detail.

```json
{
  "caption": {
    "text": "Items go on clearance after 60 days, and are thrown away after 80 days. Thus we see large drops in inventory after these events."
  },
  "annotations": [{
    "labels": [{
        "point": "inventory_items.count-60-

79",
        "text": "Clearance sale"
      },
      {
        "point": "inventory_items.count-80+",
        "text": "Thrown away"
      }
    ]
  }]
}
```

#### Add Vertical Reference Bands

To add a vertical reference band, use the `xAxis.plotBands` attribute.

The following HighCharts JSON adds a vertical reference band between November 24, 2022 and November 29, 2022 to denote a sale period. It also adds a caption to the bottom of the chart to explain the significance of the band.

Note that the `to` and `from` attributes of `xAxis.plotBands` must correspond to data values in the chart. In this example, since the data is time-based, the attributes accept Unix timestamp values (1669680000000 for November 29, 2022 and 1669248000000 for November 24, 2022). String-based date formats like MM/DD/YYYY and DD-MM-YY are not supported in the `to` and `from` HighCharts attributes.

```json
{
  "caption": {
    "text": "This chart uses the HighCharts plotBands attribute to display a band around the Black Friday Cyber Monday sale period."
  },
  "xAxis": {
    "plotBands": [{
      "to": 1669680000000,
      "from": 1669248000000,
      "label": {
        "text": "BFCM Sale Period"
      }
    }]
  }
}
```

#### Color the Maximum, Minimum, and Percentile Values

See the [Getting the most out of Looker visualizations cookbook: Conditional formatting customization in Cartesian charts](https://cloud.google.com/looker/docs/visualizations-custom-chart-editor) page for an in-depth example about coloring the maximum, minimum, and percentile values of a Cartesian visualization.