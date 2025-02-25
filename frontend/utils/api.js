#utils/ (Helper functions)
#utils/
#api.js
### Frontend API Utility (frontend/utils/api.js)
```javascript
export const fetchData = async (endpoint) => {
    const response = await fetch(`https://api.dsp.tecx.ai/${endpoint}`);
    return response.json();
};
```
