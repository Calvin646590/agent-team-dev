'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { capitalize, truncate, slugify, slugifyUnique } = require('../src/index.js');

test('capitalize: 首字母大写', () => {
  assert.strictEqual(capitalize('hello'), 'Hello');
  assert.strictEqual(capitalize(''), '');
});

test('truncate: 超长截断加省略号', () => {
  assert.strictEqual(truncate('hello world', 5), 'hell…');
  assert.strictEqual(truncate('hi', 5), 'hi');
});

test('slugify: 大写转小写 + 空格转连字符', () => {
  assert.strictEqual(slugify('Hello World'), 'hello-world');
  assert.strictEqual(slugify('FOO'), 'foo');
});

test('slugify: 去除特殊字符', () => {
  assert.strictEqual(slugify('Hello, World!'), 'hello-world');
  assert.strictEqual(slugify('a@b#c'), 'abc');
  assert.strictEqual(slugify('keep-1-2-3'), 'keep-1-2-3');
});

test('slugify: 边界 - 空串与非字符串', () => {
  assert.strictEqual(slugify(''), '');
  assert.strictEqual(slugify(42), 42);
  assert.strictEqual(slugify(null), null);
  assert.strictEqual(slugify(undefined), undefined);
});

test('slugifyUnique: 无重复保持原样', () => {
  assert.deepStrictEqual(
    slugifyUnique(['Hello World', 'Foo Bar']),
    ['hello-world', 'foo-bar']
  );
});

test('slugifyUnique: 重复加 -2/-3 后缀', () => {
  assert.deepStrictEqual(
    slugifyUnique(['foo', 'foo', 'foo']),
    ['foo', 'foo-2', 'foo-3']
  );
});

test('slugifyUnique: 不同输入产生相同 slug 时去重', () => {
  assert.deepStrictEqual(
    slugifyUnique(['A B', 'a-b']),
    ['a-b', 'a-b-2']
  );
});

test('slugifyUnique: 边界 - 空数组与非数组', () => {
  assert.deepStrictEqual(slugifyUnique([]), []);
  assert.strictEqual(slugifyUnique('nope'), 'nope');
  assert.strictEqual(slugifyUnique(null), null);
});
