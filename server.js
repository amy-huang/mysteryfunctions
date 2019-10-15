const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { Client } = require('pg');

var userId = 0;

// Initialize database
const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: true,
});

// Create table for log actions
client.connect();
client.query('create table actions ( id varchar(255), actionType varchar(255), time varchar(255) )', (err, res) => {
  // if (err) throw err;
  client.end();
});

// To see if table got made
client.connect();
client.query('show tables;', (err, res) => {
  // if (err) throw err;
  // for (let row of res.rows) {
  //   console.log(JSON.stringify(row));
  // }
  res.send(
    `Got this: ${res.rows} from ${req.connection.remoteAddress}`,
  );
  client.end();
});

const app = express();
const port = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Give client a unique ID to use for logging
app.post('/api/id', (req, res) => {
  res.send(
    `${userId}`,
  );
  userId += 1
});

// Stores info
app.post('/api/store', (req, res) => {
  logEvent = req.body
  client.query(`insert into actions (${req.connection.remoteAddress}, ${req.body.type}, ${req.body.time})`, (err, res) => {
    // if (err) throw err;
    res.send(
      `Got this: ${req.body} from ${req.connection.remoteAddress}`,
    );
    client.end();
  });
});

if (process.env.NODE_ENV === 'production') {
  // Serve any static files
  app.use(express.static(path.join(__dirname, 'client/build')));

  // Handle React routing, return all requests to React app
  app.get('*', function (req, res) {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
}

app.listen(port, () => console.log(`Listening on port ${port}`));
