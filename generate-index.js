const fs = require('fs');
const path = require('path');

// Directory containing the project HTML files
const projectsDir = './projects';
const outputFile = './index.html';

// Function to extract title from HTML file
function extractTitle(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const titleMatch = content.match(/<title>(.*?)<\/title>/i);
    return titleMatch ? titleMatch[1] : path.basename(filePath, '.html');
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error.message);
    return path.basename(filePath, '.html');
  }
}

// Function to generate the index.html
function generateIndex() {
  try {
    // Read all HTML files from the projects directory
    const files = fs.readdirSync(projectsDir)
      .filter(file => file.endsWith('.html'))
      .sort();

    if (files.length === 0) {
      console.log('No HTML files found in the projects directory.');
      return;
    }

    // Extract titles and create project data
    const projects = files.map(file => {
      const filePath = path.join(projectsDir, file);
      const title = extractTitle(filePath);
      return {
        file,
        title,
        path: `projects/${file}`
      };
    });

    // Generate HTML content
    const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenDemos - Project Gallery</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }
        .project-list {
            list-style: none;
            padding: 0;
        }
        .project-item {
            margin: 15px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .project-link {
            text-decoration: none;
            color: #007acc;
            font-weight: bold;
            font-size: 1.1em;
        }
        .project-link:hover {
            text-decoration: underline;
            color: #005599;
        }
        .project-count {
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>OpenDemos - Project Gallery</h1>
    <p>Various project demos in browsers (html, etc...)</p>
    <p class="project-count">Total projects: ${projects.length}</p>
    
    <ul class="project-list">
${projects.map(project => `        <li class="project-item">
            <a href="${project.path}" class="project-link">${project.title}</a>
        </li>`).join('\n')}
    </ul>
    
    <footer>
        <p><em>Generated automatically by generate-index.js</em></p>
    </footer>
</body>
</html>`;

    // Write the index.html file
    fs.writeFileSync(outputFile, htmlContent);
    console.log(`✅ Generated ${outputFile} with ${projects.length} project links`);
    
    // List the projects found
    console.log('\nProjects included:');
    projects.forEach((project, index) => {
      console.log(`${index + 1}. ${project.title}`);
    });

  } catch (error) {
    console.error('Error generating index.html:', error.message);
    process.exit(1);
  }
}

// Run the generator
console.log('🔄 Scanning projects directory and generating index.html...');
generateIndex();