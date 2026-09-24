document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('recommendation-form');
  const submitBtn = document.getElementById('submit-btn');
  const placeholder = document.getElementById('placeholder');
  const resultsList = document.getElementById('results-list');

  if (!form) return;

  form.addEventListener('submit', async function (event) {
    event.preventDefault();

    // 1. Extract user input values
    const budget = document.getElementById('budget').value;
    const category = document.getElementById('category').value;
    const requirements = document.getElementById('requirements').value;

    // 2. Update UI loading state
    submitBtn.disabled = true;
    submitBtn.textContent = 'Generating Recommendations...';
    placeholder.textContent = 'Analyzing your budget and requirements...';
    placeholder.classList.remove('hidden');
    resultsList.classList.add('hidden');

    try {
      /* 
        FastAPI Integration Endpoint:
        Update '/api/recommend' if your backend route differs.
      */
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          budget: parseFloat(budget),
          category: category,
          requirements: requirements,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      renderResults(data.recommendations);

    } catch (error) {
      console.warn('API connection failed or backend not running. Showing mock demo data:', error);

      // Fallback mock data for testing UI before connecting FastAPI backend
      setTimeout(() => {
        const mockData = [
          {
            title: "Option A (Best Value)",
            description: "Matches your requirements while staying well within budget.",
            price: `$${(budget * 0.75).toFixed(2)}`
          },
          {
            title: "Option B (Premium Choice)",
            description: "Uses your full budget for maximum performance and features.",
            price: `$${parseFloat(budget).toFixed(2)}`
          },
          {
            title: "Option C (Budget Saver)",
            description: "Cost-effective solution covering all primary features.",
            price: `$${(budget * 0.50).toFixed(2)}`
          }
        ];
        renderResults(mockData);
      }, 600);

    } finally {
      // 3. Reset button state
      submitBtn.disabled = false;
      submitBtn.textContent = 'Get AI Recommendations';
    }
  });

  // Render list of recommendation items dynamically
  function renderResults(items) {
    resultsList.innerHTML = '';

    if (!items || items.length === 0) {
      placeholder.textContent = 'No recommendations found for your criteria.';
      placeholder.classList.remove('hidden');
      return;
    }

    placeholder.classList.add('hidden');
    resultsList.classList.remove('hidden');

    items.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = 'recommendation-item';
      itemEl.innerHTML = `
        <div class="item-details">
          <h3>${escapeHTML(item.title)}</h3>
          <p>${escapeHTML(item.description)}</p>
        </div>
        <div class="item-price">${escapeHTML(item.price)}</div>
      `;
      resultsList.appendChild(itemEl);
    });
  }

  // Helper function to sanitize output text
  function escapeHTML(str) {
    return String(str).replace(/[&<>"']/g, match => {
      const escapeMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      };
      return escapeMap[match];
    });
  }
});
