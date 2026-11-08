const form = document.querySelector('#search-form');
const queryInput = document.querySelector('#query');
const list = document.querySelector('#issues');
const summary = document.querySelector('#summary');
const errorBox = document.querySelector('#error');
const handoff = document.querySelector('#handoff');
let requestVersion = 0;

function element(tag, text, className) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}

function renderIssue(issue) {
  const card = element('article', '', 'issue');
  card.setAttribute('aria-labelledby', `title-${issue.id}`);
  const title = element('h3', issue.title);
  title.id = `title-${issue.id}`;
  const badges = element('p', '');
  badges.append(element('span', issue.triage.level, 'badge'), element('span', issue.status, 'badge'));
  card.append(element('span', issue.id, 'issue-id'), title, badges, element('p', issue.description));
  card.append(element('p', `${issue.category} | ${issue.impact} impact | ${issue.affectedUsers} sample users | ${issue.ageDays} days`, 'metadata'));
  if (issue.blocked) card.append(element('p', 'Blocked workflow', 'metadata'));
  if (issue.triage.reasons.length) card.append(element('p', `Why: ${issue.triage.reasons.join('; ')}`, 'metadata'));
  return card;
}

async function loadBoard(query = '') {
  const version = ++requestVersion;
  errorBox.hidden = true;
  summary.textContent = 'Loading issues...';
  handoff.hidden = true;
  try {
    const response = await fetch(`/api/issues?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error(`Board request failed (${response.status}).`);
    const board = await response.json();
    if (version !== requestVersion) return;
    list.replaceChildren(...board.issues.map(renderIssue));
    if (!board.issues.length) list.append(element('p', 'No issues match. Try fewer words or clear the search.'));
    summary.textContent = board.summary.available
      ? `${board.summary.total} visible | ${board.summary.open} active | ${board.summary.blocked} active blocked`
      : `${board.summary.total} visible issues. Detailed counts unlock in Lab 3.`;
    if (board.summary.available) {
      summary.textContent += ` | Categories: ${Object.entries(board.summary.byCategory).map(([name, count]) => `${name} ${count}`).join(', ') || 'none'}`;
    }
    handoff.hidden = !board.handoffAvailable;
    handoff.href = `/api/handoff?q=${encodeURIComponent(query)}`;
  } catch (error) {
    if (version !== requestVersion) return;
    list.replaceChildren();
    summary.textContent = 'Board unavailable.';
    errorBox.textContent = `${error.message} Check that npm start is running, then search again.`;
    errorBox.hidden = false;
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  loadBoard(queryInput.value);
});
form.addEventListener('reset', () => loadBoard(''));
loadBoard();
