const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('e:/axomai_agi/src/axomai/api/templates/index.html', 'utf8');

const scriptRegex = /<script\b(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  const code = match[1];
  const upToMatch = html.substring(0, match.index);
  const startLine = upToMatch.split('\n').length;
  console.log(`Script block #${count} starts around line ${startLine}`);

  try {
    new vm.Script(code, { filename: 'index.html', lineOffset: startLine });
    console.log(`Block #${count}: Valid!`);
  } catch (err) {
    console.error(`ERROR in block #${count}:`, err.message);
    console.error(`Stack:`, err.stack);
  }
}
