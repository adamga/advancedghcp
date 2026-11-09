export const issues = [
  { id: 'ISS-101', title: 'Checkout stops on an empty basket', description: 'A fictional demo store shows an error instead of an empty-basket hint.', category: 'payments', status: 'open', impact: 'high', affectedUsers: 140, blocked: true, ageDays: 8 },
  { id: 'ISS-102', title: 'Keyboard focus disappears in the menu', description: 'Tab navigation skips a fictional product menu after it opens.', category: 'accessibility', status: 'open', impact: 'medium', affectedUsers: 45, blocked: true, ageDays: 3 },
  { id: 'ISS-103', title: 'Export heading has a typo', description: 'The sample CSV heading says catgory instead of category.', category: 'reporting', status: 'open', impact: 'low', affectedUsers: 12, blocked: false, ageDays: 9 },
  { id: 'ISS-104', title: 'Search ignores uppercase words', description: 'Searching for BLUE misses a synthetic item called Blue notebook.', category: 'search', status: 'in-progress', impact: 'medium', affectedUsers: 110, blocked: false, ageDays: 2 },
  { id: 'ISS-105', title: 'Receipt uses the wrong sample currency', description: 'A fictional receipt shows credits rather than demo points.', category: 'payments', status: 'closed', impact: 'high', affectedUsers: 200, blocked: true, ageDays: 14 },
  { id: 'ISS-106', title: 'Small-screen chart overlaps its legend', description: 'The sample reporting chart is hard to read on a narrow screen.', category: 'reporting', status: 'in-progress', impact: 'medium', affectedUsers: 80, blocked: false, ageDays: 7 },
  { id: 'ISS-107', title: 'Image alternative text is missing', description: 'A decorative demo image is announced as an unhelpful file name.', category: 'accessibility', status: 'open', impact: 'low', affectedUsers: 25, blocked: false, ageDays: 1 },
  { id: 'ISS-108', title: 'Saved search loses its label', description: 'A fictional saved-search label disappears after a page refresh.', category: 'search', status: 'closed', impact: 'low', affectedUsers: 5, blocked: false, ageDays: 4 }
].map((issue) => Object.freeze(issue));

Object.freeze(issues);
