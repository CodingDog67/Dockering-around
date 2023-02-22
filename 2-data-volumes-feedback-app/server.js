/*
This will create a server that allows users to input feedback to sth with a title and text. 
If feedback is submitted it is first stored in two files temp and final, check if exist in final and if not
copy temp to final file path (temp and feedback folders)

see the files by adding /feedback/name_of_feedback to local host 
you cannot see the files on local machine, only in container file system == /app
*/



const fs = require('fs').promises;
const exists = require('fs').exists;
const path = require('path');

const express = require('express');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

app.use(express.static('public'));
app.use('/feedback', express.static('feedback'));

app.get('/', (req, res) => {
  const filePath = path.join(__dirname, 'pages', 'feedback.html');
  res.sendFile(filePath);
});

app.get('/exists', (req, res) => {
  const filePath = path.join(__dirname, 'pages', 'exists.html');
  res.sendFile(filePath);
});

app.post('/create', async (req, res) => {
  const title = req.body.title;
  const content = req.body.text;

  const adjTitle = title.toLowerCase();

  const tempFilePath = path.join(__dirname, 'temp', adjTitle + '.txt');
  const finalFilePath = path.join(__dirname, 'feedback', adjTitle + '.txt');

  // This line is to test the ability of docker to manage real time changes
  // Should be visible with "docker logs feedback-app", stop, start again is an option
  // or 
  console.log('Kiki scolds')

  await fs.writeFile(tempFilePath, content);
  exists(finalFilePath, async (exists) => {
    if (exists) {
      res.redirect('/exists');
    } else {
      await fs.copyFile(tempFilePath, finalFilePath);
      await fs.unlink(tempFilePath);
      res.redirect('/');
    }
  });
});

// changed from 80 to process.env.PORT to showcase use of ENV vars
app.listen(process.env.PORT);
