(function(){
  const el=document.getElementById('timer'); if(!el) return;
  
  const secName = typeof SECTION_NAME !== 'undefined' ? SECTION_NAME.replace(/[^a-zA-Z0-9]/g, '_') : 'General';
  const attId = typeof ATTEMPT_ID !== 'undefined' ? ATTEMPT_ID : '0';
  
  const key = `cgaat_test_end_time_att_${attId}_sec_${secName}`;
  let end=localStorage.getItem(key);
  
  if(!end){ 
      end = Date.now() + 10*60*1000; 
      localStorage.setItem(key, end); 
  }
  
  const startKey = `cgaat_test_start_att_${attId}`;
  let testStart = localStorage.getItem(startKey);
  if (!testStart) {
      testStart = Date.now();
      localStorage.setItem(startKey, testStart);
  }
  
  const warningKey = `cgaat_test_warn_att_${attId}_sec_${secName}`;
  let warningShown = localStorage.getItem(warningKey) === 'true';
  
  function tick(){
    let left=Math.max(0, parseInt(end)-Date.now());
    let m=Math.floor(left/60000), s=Math.floor((left%60000)/1000);
    el.textContent=String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');

    let timeUsedMs = Date.now() - parseInt(testStart);
    let usedM = Math.floor(timeUsedMs / 60000);
    let usedS = Math.floor((timeUsedMs % 60000) / 1000);
    const usedEl = document.getElementById('time-used-display');
    if (usedEl) {
        usedEl.textContent = String(usedM).padStart(2,'0') + ':' + String(usedS).padStart(2,'0');
    }

    if (left <= 5 * 60 * 1000) {
        el.style.color = '#dc2626'; // Red color
        el.style.fontWeight = 'bold';
    }

    if (left <= 2 * 60 * 1000 && left > 0 && !warningShown) {
        alert("Only 2 minutes left");
        warningShown = true;
        localStorage.setItem(warningKey, 'true');
    }

    if(left<=0){ 
        const form = document.getElementById('qform');
        if (form) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'submit';
            input.value = '1';
            form.appendChild(input);
            form.submit();
        }
    }
  }
  
  tick(); 
  setInterval(tick, 1000);
})();
