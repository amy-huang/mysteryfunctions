# Mystery Functions

The first iteration of Mystery Functions was implemented by Amy Huang for her computer science honors thesis at Brown in the 2019-2020 school year. The writeup can be found here: [Mystery Functions](https://cs.brown.edu/research/pubs/theses/ugrad/2020/huang.amy.pdf).

The `functions` branch of this repo is Mystery Functions, and the `master` branch of this repo is Mystery Predicates. The master branch has the most cleaned up and commented source files.

Both versions of the web application consist of a node.js server and a React client; it is deployed on Heroku with a Postgres database.

The `client/` directory contains the React client. The client can be started remotely from the `client/` directory using yarn: “yarn start” on port 300.

Upon startup, the server creates a new connection pool for the clients to connect to, the actions table where actions will be logged if it doesn’t exist yet, and starts listening on port 5000.

It accepts JSON objects at `/api/store` that represent user actions, and stores the data as a database row accordingly. Here is a description of the `actions` database schema, according to the type of action being recorded as a row.
|  Column Name |          Data Type          |                                     Meaning of column for Input Evaluation                                     |                                        Meaning of column for Quiz Answer                                       |                                         Meaning of column for Final Guess                                        |
|:------------:|:---------------------------:|:--------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------:|
|    userid    |   character varying(255)    | Subject’s school ID (e.g. cs login) for identifying actions from their session and giving them academic credit | Subject’s school ID (e.g. cs login) for identifying actions from their session and giving them academic credit |  Subject’s school ID (e.g. cs login) for identifying actions from their session and giving them academic credit  |
|    fcnname   |   character varying(255)    |                                              Name of the function                                              |                                              Name of the function                                              |                                               Name of the function                                               |
|   actionid   |           integer           |                 Number of the action (starts at 0, increments by 1 for each successive action)                 |                 Number of the action (starts at 0, increments by 1 for each successive action)                 |                  Number of the action (starts at 0, increments by 1 for each successive action)                  |
|  actiontype  |   character varying(255)    |                                                   eval_input                                                   |                                                   quiz_answer                                                  |                                                   final_answer                                                   |
|     time     | timestamp without time zone |                       Local browser time without timezone (Indiana, Brown were both EST)                       |                        Local browser time without timezone (Indiana, Brown were both EST                       |                         Local browser time without timezone (Indiana, Brown were both EST                        |
|     input    |   character varying(255)    |                                                 Input evaluated                                                |                            Quiz question input that subject submitted an output for                            |                                                     Not used                                                     |
|    output    |   character varying(255)    |                                                Resulting output                                                |                                           Output submitted by subject                                          |                                                     Not used                                                     |
|     quizq    |           integer           |                                                    Not used                                                    |                                         # of quiz question (0, 1 or 2)                                         |                                                     Not used                                                     |
| actualoutput |   character varying(255)    |                                                    Not used                                                    |                                           Actual output of the input                                           |                                                     Not used                                                     |
|    result    |           boolean           |                                                    Not used                                                    |                                      Whether the output given was correct                                      |                                                     Not used                                                     |
|  finalguess  |   character varying(255)    |                                                    Not used                                                    |                                                    Not used                                                    | Text submitted of the subject’s last guess about what the function does before they move on to the next function |

The analysis was done by downloading the database rows from Heroku as CSV files, and then using Python3 to parse them and calculate metrics. The answer labels were parsed as CSV files as well. The code to do so can be found in `analysis/`.
