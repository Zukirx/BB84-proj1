// static/app.js
const qubitRange = document.getElementById('qubitRange');
const rangeValue = document.getElementById('rangeValue');
const runBtn = document.getElementById('runBtn');

qubitRange.addEventListener('input', (e) => {
    rangeValue.textContent = e.target.value;
});

runBtn.addEventListener('click', async () => {
    runBtn.disabled = true;
    runBtn.textContent = "COMPUTING QUANTUM PIPELINE...";

    const numQubits = qubitRange.value;
    const activeEve = document.getElementById('eveToggle').checked;

    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ num_qubits: numQubits, active_eve: activeEve })
        });

        const data = await response.json();

        // 1. Telemetry indicators
        const yieldRate = ((data.sifted_indices.length / numQubits) * 100).toFixed(1);
        document.getElementById('yieldMetric').textContent = `${yieldRate}%`;
        document.getElementById('qberMetric').textContent = `${data.qber}%`;

        const statusMetric = document.getElementById('statusMetric');
        const aliceHashEl = document.getElementById('aliceHash');
        const bobHashEl = document.getElementById('bobHash');

        aliceHashEl.textContent = data.alice_hash;

        if (data.intrusion_alert) {
            statusMetric.textContent = "🚨 ALARM: INTRUSION";
            statusMetric.className = "status-badge alert";
            bobHashEl.textContent = "COMPROMISED DATA POOL // INTERCEPTION FLUSH DETECTED";
            bobHashEl.className = "hash-box alert-text";
        } else {
            statusMetric.textContent = "🛡️ SECURE LINE";
            statusMetric.className = "status-badge secure";
            bobHashEl.textContent = data.bob_hash;
            bobHashEl.className = "hash-box";
        }

        // 2. RENDER NEW PUBLIC SECURITY AUDIT ROW (Up to 20 bits max)
        const auditContainer = document.getElementById('securityCheckContainer');
        auditContainer.innerHTML = '';

        if (data.sample_indices.length === 0) {
            auditContainer.innerHTML = '<div class="tile-label" style="padding: 1rem;">No bits selected for sample distribution. Increase qubits stream length.</div>';
        } else {
            const displayAuditLimit = Math.min(20, data.sample_indices.length);
            for (let idx = 0; idx < displayAuditLimit; idx++) {
                const globalPos = data.sample_indices[idx];
                const auditTile = document.createElement('div');
                auditTile.className = 'photon-tile audit-tile';

                const bitMismatched = data.a_bits[globalPos] !== data.b_bits[globalPos];
                const cmpClass = bitMismatched ? 'mismatch-highlight' : 'match-highlight';
                const verdictString = bitMismatched ? '❌ ERROR' : '✅ VALID';

                auditTile.innerHTML = `
                    <div class="tile-index-marker">#${globalPos}</div>
                    <div class="node-group">
                        <div class="tile-label">Values</div>
                        <div class="audit-comparison">
                            A: <b>${data.a_bits[globalPos]}</b> | B: <b>${data.b_bits[globalPos]}</b>
                        </div>
                        <div class="tile-flag ${cmpClass}" style="border:none; padding:0; width:100%; font-size:0.8rem;">
                            ${verdictString}
                        </div>
                    </div>
                `;
                auditContainer.appendChild(auditTile);
            }
        }

        // 3. Render traditional Horizontal Telemetry Wire Map
        const container = document.getElementById('photonWireContainer');
        container.innerHTML = '';

        const renderLimit = Math.min(16, numQubits);
        for (let i = 0; i < renderLimit; i++) {
            const tile = document.createElement('div');
            const aBasisIcon = data.a_bases[i] === 'Z' ? '↕ (Z)' : '⤢ (X)';
            const bBasisIcon = data.b_bases[i] === 'Z' ? '↕ (Z)' : '⤢ (X)';

            let isCorrupted = activeEve && (data.a_bits[i] !== data.b_bits[i]) && data.sifted_indices.includes(i);
            tile.className = `photon-tile ${isCorrupted ? 'state-corrupted' : ''}`;

            let eveHTML = '';
            if (activeEve) {
                const eBasisIcon = data.eve_bases[i] === 'Z' ? '↕ (Z)' : '⤢ (X)';
                eveHTML = `
                    <div class="node-group">
                        <div class="tile-label">Eve Intercept</div>
                        <div class="quantum-state-node" style="border-color: var(--neon-amber);">${data.eve_bits[i]}</div>
                        <div class="tile-label" style="font-family: monospace; font-size: 0.7rem;">${eBasisIcon}</div>
                    </div>
                `;
            }

            let flagText = 'Discard';
            let flagClass = 'drop';
            if (data.sample_indices.includes(i)) {
                flagText = 'Sample';
                flagClass = 'check';
            } else if (data.sifted_indices.includes(i)) {
                flagText = 'Sifted';
                flagClass = 'match';
            }

            tile.innerHTML = `
                <div class="tile-index-marker">#${i}</div>
                <div class="node-group">
                    <div class="tile-label">Alice Encoder</div>
                    <div class="quantum-state-node">${data.a_bits[i]}</div>
                    <div class="tile-label" style="font-family: monospace; font-size: 0.7rem;">${aBasisIcon}</div>
                </div>
                ${eveHTML}
                <div class="node-group">
                    <div class="tile-label">Bob Measure</div>
                    <div class="quantum-state-node" style="${isCorrupted ? 'border-color: var(--neon-red);' : 'border-color: var(--neon-green);'}">${data.b_bits[i]}</div>
                    <div class="tile-label" style="font-family: monospace; font-size: 0.7rem;">${bBasisIcon}</div>
                </div>
                <div class="tile-flag ${flagClass}">${flagText}</div>
            `;
            container.appendChild(tile);
        }
    } catch (err) {
        console.error("Simulation error:", err);
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = "▶️ RUN PROTOCOL";
    }
});