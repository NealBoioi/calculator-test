const display = document.getElementById('display');
const buttons = document.querySelectorAll('.button');

function updateDisplay(value) {
  if (display.value === '0' && value !== '.') {
    display.value = value;
  } else {
    display.value += value;
  }
}

function sanitizeExpression(expression) {
  return expression.replace(/×/g, '*').replace(/÷/g, '/');
}

function calculate() {
  const expression = sanitizeExpression(display.value);
  if (!/^[0-9.+\-*/()%\s]+$/.test(expression)) {
    display.value = 'Error';
    return;
  }

  try {
    const result = Function(`"use strict"; return (${expression})`)();
    display.value = String(result);
  } catch {
    display.value = 'Error';
  }
}

function clearDisplay() {
  display.value = '0';
}

function deleteLast() {
  display.value = display.value.length > 1 ? display.value.slice(0, -1) : '0';
}

function percent() {
  try {
    const value = parseFloat(display.value.replace(/×/g, '*').replace(/÷/g, '/'));
    display.value = String(value / 100);
  } catch {
    display.value = 'Error';
  }
}

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const value = button.dataset.value;
    const action = button.dataset.action;

    if (action === 'clear') {
      clearDisplay();
      return;
    }

    if (action === 'delete') {
      deleteLast();
      return;
    }

    if (action === 'percent') {
      percent();
      return;
    }

    if (action === 'equals') {
      calculate();
      return;
    }

    updateDisplay(value);
  });
});
