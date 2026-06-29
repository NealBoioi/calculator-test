(function (root, factory) {
  const api = factory();

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }

  root.CalculatorApp = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  function sanitizeExpression(expression) {
    return expression.replace(/×/g, '*').replace(/÷/g, '/');
  }

  function formatResult(value) {
    if (!Number.isFinite(value)) {
      return 'Error';
    }

    const rounded = Math.round(value * 1e12) / 1e12;
    return String(rounded);
  }

  function evaluateExpression(expression) {
    const sanitized = sanitizeExpression(expression);

    if (!/^[0-9.+\-*/()%\s]+$/.test(sanitized)) {
      return 'Error';
    }

    try {
      const result = Function('"use strict"; return (' + sanitized + ')')();
      return Number.isFinite(result) ? result : 'Error';
    } catch {
      return 'Error';
    }
  }

  function createCalculator(rootElement = document) {
    const display = rootElement.getElementById('display');
    const buttons = rootElement.querySelectorAll('.button');

    let expression = '0';
    let lastAction = 'clear';

    function updateDisplay(value) {
      expression = value;
      display.value = value;
    }

    function appendDigit(value) {
      if (display.value === 'Error') {
        updateDisplay(value === '.' ? '0.' : value);
        lastAction = 'number';
        return;
      }

      if (lastAction === 'equals') {
        updateDisplay(value === '.' ? '0.' : value);
        lastAction = 'number';
        return;
      }

      if (expression === '0' && value !== '.') {
        updateDisplay(value);
      } else if (expression === '0' && value === '.') {
        updateDisplay('0.');
      } else if (value === '.' && expression.slice(-1) === '.') {
        return;
      } else {
        updateDisplay(expression + value);
      }

      lastAction = 'number';
    }

    function appendOperator(operator) {
      if (display.value === 'Error') {
        updateDisplay('0');
      }

      if (expression === '0' && operator === '-') {
        updateDisplay('-');
        lastAction = 'operator';
        return;
      }

      if (lastAction === 'operator') {
        updateDisplay(expression.slice(0, -1) + operator);
      } else {
        updateDisplay(expression + operator);
      }

      lastAction = 'operator';
    }

    function clearDisplay() {
      updateDisplay('0');
      lastAction = 'clear';
    }

    function deleteLast() {
      if (display.value === 'Error') {
        clearDisplay();
        return;
      }

      const next = expression.length > 1 ? expression.slice(0, -1) : '0';
      updateDisplay(next);
      lastAction = 'delete';
    }

    function percent() {
      if (display.value === 'Error') {
        clearDisplay();
        return;
      }

      const numericValue = Number.parseFloat(expression);
      if (Number.isNaN(numericValue)) {
        updateDisplay('Error');
        return;
      }

      updateDisplay(String(numericValue / 100));
      lastAction = 'percent';
    }

    function calculate() {
      const result = evaluateExpression(expression);
      updateDisplay(typeof result === 'number' ? formatResult(result) : result);
      lastAction = 'equals';
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

        if (value && /[0-9.]/.test(value)) {
          appendDigit(value);
          return;
        }

        if (value && /[+\-×÷]/.test(value)) {
          appendOperator(value);
        }
      });
    });

    return {
      evaluateExpression,
      clearDisplay,
      deleteLast,
      percent,
      calculate,
    };
  }

  return {
    evaluateExpression,
    createCalculator,
  };
});

if (typeof document !== 'undefined') {
  CalculatorApp.createCalculator();
}
