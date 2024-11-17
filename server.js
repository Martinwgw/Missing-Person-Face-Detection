const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const multer = require('multer');
const path = require('path');
const app = express();

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));

// MySQL connection configuration
const db = mysql.createConnection({
    host: 'localhost',      
    user: 'root',           
    password: 'root',           
    database: 'miniproject_db' 
});

// Connect to MySQL
db.connect((err) => {
    if (err) throw err;
    console.log('Connected to MySQL database');
});

// Serve static files (HTML, CSS)
app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'project_loginpage.html')); 
}); 

// Handle login requests
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    console.log("Received username (email):", username);
    console.log("Received password:", password);

    const query = "SELECT * FROM user WHERE Username = ? AND Password = ?";
    db.query(query, [ username, password], (err, results) => {
        if (err) {
            console.error('Error executing query:', err.message);
            res.status(500).send('Internal Server Error');
            return;
        }

        console.log("Query results:", results); // Log the results for debugging    

        if (results.length > 0) {
            // res.send('Login successful!');
            res.redirect('project_missingperson_registraionfrom.html');
        } else {
            res.send('Invalid username or password');
        }
    });
});

// Configure file storage for Multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        
        const folder = file.mimetype.startsWith('image') ? 'uploads/photos' : 'uploads/videos';
        cb(null, folder);
    },
    filename: (req, file, cb) => {
        
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

// Initialize the multer instance
const upload = multer({ storage: storage });
const BASE_URL = "http://localhost:3000/";

// Route to handle missing person form submission
app.post('/submit_missing_person', upload.fields([{ name: 'photo' }, { name: 'video' }]), (req, res) => {
    const { name, dob, gender, last_seen, date_missing, description } = req.body;

    // Get file paths
    const photo_path = req.files['photo'] ? BASE_URL + req.files['photo'][0].path : null;
    const video_path = req.files['video'] ? BASE_URL + req.files['video'][0].path : null;

    // SQL query to insert data
    const query = `INSERT INTO missing_person_details (Full_name, DOB, Gender, Last_location, Date_missing, Description, Photo_path, Video_path)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)`;

    db.query(query, [name, dob, gender, last_seen, date_missing, description, photo_path, video_path], (err, result) => {
        if (err) {
            console.error('Error inserting data:', err.message);
            res.status(500).send('Failed to submit missing person details');
        } else {
            res.send('Missing person details submitted successfully');
        }
    });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
