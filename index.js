const express = require('express');
var cors = require('cors');
const app = express();

// CORS
app.use(cors());

// Serves Express Yourself website
app.use(express.static('public'));

// Set a port number
const port = process.env.PORT || 4001;

// Permits localhost requests
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});

// Redirects homepage to the /annotations homepage
app.get('/', function (req, res) {
    res.redirect('/annotations');
});

/**
 * Returns random 10 annotations
 * @param {number} id
 * @returns {Object}
 */
app.get('/annotations', (req, res, next) => {
    let page = 0
    page = parseInt(req.query.page, 10)
    const skip = page * 10
    var query = {};
    collection.find(query).limit(10).skip(skip).toArray(function (err, result) {
        if (err) throw err;
        res.send(result)
    });
});

/**
 * Search annotations that has the keyword 
 * @param {string} keyword
 * @returns {Object}
 */
app.get('/annotations/search/:keyword', (req, res, next) => {
    // get query param for keyword
    var query = { 'target.selector.exact': req.params.keyword };

    // Fethces 10 annotations from the database
    collection.find(query).limit(10).toArray(function (err, result) {
        if (err) throw err;
        if (result.length > 0) {
            res.send(result)
        } else {
            res.send({ 'message': 'Not Found' }).status(204)
        }

    });
});

/**
 * Returns an annotation object
 * @param {number} id
 * @returns {Object}
 */
app.get('/annotations/:id', (req, res, next) => {
    // Get an annotatition from the database
    collection.findOne({ id: { $regex: '/' + req.params.id } }, function (err, result) {
        if (err) throw err
        if (result) {
            res.send(result)
        }
        else {
            res.status(404).send({ 'message': 'Not Found' })
        }
    })
});

/**
 * Given article id, returns all annotations of the article
 * @param {number} id
 * @returns {Object}
 */
app.get('/annotations/pmid/:id', (req, res, next) => {
    // gets all annotaions of the article from the database
    collection.find({ 'target.source': { $regex: '/' + req.params.id } }).toArray(function (err, result) {
        if (err) throw err
        if (result.length > 0) {
            res.send(result)
        } else {
            res.status(404).send({ 'message': 'Not Found' })
        }

    })
});

/**
 * Given an article returns only labels
 * @param {number} id
 * @returns {Array}
 */
app.get('/annotations/pmid/:id/label', (req, res, next) => {
    // gets a summary annotation data for the article
    collection.find(
        { 'target.source': { $regex: '/' + req.params.id } },
        { projection: { _id: 0, id: 1, 'target.selector.exact': 1 } })
        .toArray(function (err, result) {
            if (err) throw err
            if (result.length > 0) {
                res.send(result)
            } else {
                res.status(404).send({ 'message': 'Not Found' })
            }
        })
});

/**
 * Given an article returns only targets
 * @param {number} id
 * @returns {Array}
 */
app.get('/annotations/pmid/:id/target', (req, res, next) => {
    collection.find(
        { 'target.source': { $regex: '/' + req.params.id } },
        { projection: { _id: 0, id: 1, 'target': 1 } })
        .toArray(function (err, result) {
            if (err) throw err
            if (result.length > 0) {
                res.send(result)
            } else {
                res.status(404).send({ 'message': 'Not Found' })
            }git
        })
});

/**
 * Connect database and keep the connection
 * @param {string} db
 * @param {string} collection 
 * @param {string} mongo_uri
 * @returns {Object} a connection object
 */
var MongoClient = require('mongodb').MongoClient
let db;
let collection;
const mongo_uri = "mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net"

MongoClient
    .connect(mongo_uri, { useNewUrlParser: true, poolSize: 10, useUnifiedTopology: true })
    .then(client => {
        db = client.db('annotations');
        collection = db.collection('annotations');

        app.listen(port, () => {
            console.log(`listening on port ${port}`)
        })
    })
    .catch(error => console.error(error));
