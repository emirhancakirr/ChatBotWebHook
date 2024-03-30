"use strict";

const express = require("express");
const bodyParser = require("body-parser");
const JiraClient = require("jira-connector"); // Import the Jira client library

const app = express().use(bodyParser.json());


app.get("/", (req, res) => {
  if (req.query.token !== token) {
    return res.sendStatus(401);
  }

  return res.end(req.query.challenge);
});

app.post("/", (req, res) => {
  if (req.query.token !== token) {
    return res.sendStatus(401);
  }

  console.log(req.body);

  const issueKey =  req.body.attributes["track-it"]
  // Example usage of the function
  getJiraIssueDetails(issueKey, (error, issue) => {

    if (error) {
      console.log(" couldn't found and send to the client");
      const data = {
        responses: [
          {
            "type": "text",
            "message": `couldn't fetch issue details:`
          }
        ]
      };
      res.json(data);
    } else {
      console.log("Issue found and send to the client");
      const data = {
        responses: [
          {
            "type": "text",
            "message": `${issue.key}: ${issue.fields.summary}\n${issue.fields.description}\n${issue.fields.status.name}`
          }
        ]
      };
      console.log(data);
      res.json(data);
    }
  });
});

// Function to fetch details of a single issue by its key
function getJiraIssueDetails(issueKey, callback) {
  const jira = new JiraClient({
    host: "ku-ecakir20.atlassian.net", // Remove 'https://'
    basic_auth: {
      email: "ecakir20@ku.edu.tr",
      api_token:
        "ATATT3xFfGF0GGmmVcjAw0IEgmBHp5d_5jc6vqMC03zf62bxXtAWqAwf8EJ0x81zZr90tf-U9ain8AqxbgWrbtcGj4XFzHb70Cim5sWt5wNpi9zTF2bSWakq4DSLe-ZP_aoAxwD5U9D1fYA_mMl12fy3DoeHaBmXwz0RWbzp79FYtjf93UGPW5c=66120A4D",
    },
  });

  jira.issue.getIssue({ issueKey }, (error, issue) => {
    if (error) {
      console.error("Error:", error);
      callback(error, null);
    } else {
      callback(null, issue);
    }
  });
}

app.listen(3000, () => console.log("[ChatBot] Webhook is listening"));
