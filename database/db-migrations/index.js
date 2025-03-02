const fs = require('fs');
const { exporter } = require('@dbml/core');

// get DBML file content
const dbml = fs.readFileSync('./schema.dbml', 'utf-8');

// generate MySQL from DBML
const sql = exporter.export(dbml, 'postgres');

fs.writeFile('migration.sql', sql, err => {
  if (err) {
    console.error(err);
  } else {
    console.log('File written successfully');
  }
});

