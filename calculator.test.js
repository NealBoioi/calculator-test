const test = require('node:test');
const assert = require('node:assert/strict');
const { evaluateExpression } = require('./script.js');

test('evaluates basic arithmetic with operator precedence', () => {
  assert.equal(evaluateExpression('2+3*4'), 14);
});

test('evaluates decimal arithmetic correctly', () => {
  assert.equal(evaluateExpression('10.5+2.25'), 12.75);
});

test('evaluates division and multiplication in sequence', () => {
  assert.equal(evaluateExpression('12/3*4'), 16);
});
