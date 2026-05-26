'use strict';

/**
 * Capitalize the first character of a string.
 * @param {string} s
 * @returns {string}
 */
function capitalize(s) {
  if (typeof s !== 'string' || s.length === 0) return s;
  return s[0].toUpperCase() + s.slice(1);
}

/**
 * Truncate a string to at most n characters, appending an ellipsis if cut.
 * @param {string} s
 * @param {number} n
 * @returns {string}
 */
function truncate(s, n) {
  if (typeof s !== 'string') return s;
  if (s.length <= n) return s;
  return s.slice(0, Math.max(0, n - 1)) + '…';
}

/**
 * Convert a string into a URL-friendly slug.
 * Lowercases, turns spaces into hyphens, and strips any character
 * that is not in [a-z0-9-]. Spaces are not collapsed.
 * @param {string} s
 * @returns {string}
 */
function slugify(s) {
  if (typeof s !== 'string') return s;
  if (s.length === 0) return '';
  return s
    .toLowerCase()
    .replace(/ /g, '-')
    .replace(/[^a-z0-9-]/g, '');
}

/**
 * Slugify an array of strings, ensuring every resulting slug is unique.
 * Each element is passed through {@link slugify}. When a slug collides with
 * an earlier one, a numeric suffix is appended: the second occurrence gets
 * `-2`, the third `-3`, and so on.
 * @param {string[]} strs
 * @returns {string[]}
 */
function slugifyUnique(strs) {
  if (!Array.isArray(strs)) return strs;
  const counts = Object.create(null);
  return strs.map((s) => {
    const base = slugify(s);
    const seen = counts[base] || 0;
    counts[base] = seen + 1;
    return seen === 0 ? base : base + '-' + (seen + 1);
  });
}

module.exports = { capitalize, truncate, slugify, slugifyUnique };
