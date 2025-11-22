document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analyzeForm');
    const resumeInput = document.getElementById('resumeUpload');
    const fileListDisplay = document.getElementById('fileList');
    const submitBtn = document.getElementById('submitBtn');
    const btnLoader = document.getElementById('btnLoader');
    const btnText = submitBtn.querySelector('.btn-text');
    const resultsContent = document.getElementById('resultsContent');
    const candidatesList = document.getElementById('candidatesList');
    const jdText = document.getElementById('jdText');
    const charCount = document.getElementById('charCount');
    const statResumes = document.getElementById('statResumes');

    let scoreChartInstance = null;
    let sectorChartInstance = null;
    let allFiles = [];

    if (jdText && charCount) {
        jdText.addEventListener('input', (e) => {
            charCount.textContent = e.target.value.length;
        });
    }

    resumeInput.addEventListener('change', (e) => {
        const newFiles = Array.from(e.target.files);
        allFiles = [...allFiles, ...newFiles];
        updateFileList();

        const addMoreBtn = document.getElementById('addMoreBtn');
        if (allFiles.length > 0) {
            addMoreBtn.style.display = 'block';
        }
    });

    document.getElementById('addMoreBtn').addEventListener('click', () => {
        resumeInput.click();
    });

    function updateFileList() {
        fileListDisplay.innerHTML = '';
        if (allFiles.length > 0) {
            allFiles.forEach((file, index) => {
                const div = document.createElement('div');
                div.className = 'file-item';
                div.innerHTML = `
                    <span>${file.name}</span>
                    <button type="button" class="remove-file-btn" data-index="${index}">✕</button>
                `;
                fileListDisplay.appendChild(div);
            });

            document.querySelectorAll('.remove-file-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const index = parseInt(e.target.getAttribute('data-index'));
                    allFiles.splice(index, 1);
                    updateFileList();

                    if (allFiles.length === 0) {
                        document.getElementById('addMoreBtn').style.display = 'none';
                    }
                });
            });
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const jdTextValue = document.getElementById('jdText').value;

        if (allFiles.length === 0 || !jdTextValue) {
            alert("Please upload resumes and enter a job description.");
            return;
        }

        setLoading(true);

        const formData = new FormData();
        allFiles.forEach(file => {
            formData.append('resumes', file);
        });
        formData.append('jd_text', jdTextValue);

        try {
            const response = await fetch('/api/score', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error(error);
            alert('Something went wrong. Please try again.');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            if (btnText) btnText.style.opacity = '0';
            btnLoader.style.display = 'block';
        } else {
            submitBtn.disabled = false;
            if (btnText) btnText.style.opacity = '1';
            btnLoader.style.display = 'none';
        }
    }

    function displayResults(results) {
        resultsContent.classList.remove('hidden');
        resultsContent.scrollIntoView({ behavior: 'smooth' });

        if (statResumes) {
            statResumes.textContent = results.filter(r => !r.error).length;
        }

        const scores = results.map(r => r.score).filter(s => s !== undefined);
        const degrees = results.map(r => r.degree).filter(d => d !== undefined);

        renderScoreChart(scores);
        renderDegreeChart(degrees);

        candidatesList.innerHTML = '';
        results.sort((a, b) => b.score - a.score);

        results.forEach(res => {
            if (res.error) return;

            const card = document.createElement('div');
            card.className = 'candidate-card';

            let scoreClass = 'score-low';
            let suggestion = "Consider other candidates";
            let suggestionClass = 'suggestion-low';
            let suggestionIcon = '⚠️';

            if (res.score === 100) {
                scoreClass = 'score-high';
                suggestion = "Perfect Match! Meets all requirements";
                suggestionClass = 'suggestion-high';
                suggestionIcon = '🌟';
            } else if (res.score >= 80) {
                scoreClass = 'score-high';
                suggestion = "Excellent Match! Highly recommended";
                suggestionClass = 'suggestion-high';
                suggestionIcon = '✨';
            } else if (res.score >= 60) {
                scoreClass = 'score-med';
                suggestion = "Good Match! Consider for interview";
                suggestionClass = 'suggestion-med';
                suggestionIcon = '👍';
            } else if (res.score >= 40) {
                scoreClass = 'score-med';
                suggestion = "Potential Match! May require training";
                suggestionClass = 'suggestion-med';
                suggestionIcon = '💡';
            }

            const keywordsHTML = res.missing_keywords.length === 0
                ? '<div class="keyword-chip keyword-perfect">✅ All Requirements Met</div>'
                : res.missing_keywords.slice(0, 5).map(kw =>
                    `<div class="keyword-chip keyword-missing">${kw}</div>`
                ).join('');

            const technicalSkillsHTML = res.skills && res.skills.technical.length > 0
                ? res.skills.technical.map(skill =>
                    `<span class="skill-badge skill-technical">${skill}</span>`
                ).join('')
                : '<span class="skill-badge skill-none">No tech skills found</span>';

            const softSkillsHTML = res.skills && res.skills.soft.length > 0
                ? res.skills.soft.map(skill =>
                    `<span class="skill-badge skill-soft">${skill}</span>`
                ).join('')
                : '';

            card.innerHTML = `
                <div class="candidate-info">
                    <div class="candidate-header">
                        <h4>${res.filename}</h4>
                        <div class="rank-badge">#${results.indexOf(res) + 1}</div>
                    </div>
                    
                    <div class="candidate-meta">
                        <span class="meta-tag">
                            <span class="meta-icon">📂</span>
                            ${res.category}
                        </span>
                        <span class="meta-tag">
                            <span class="meta-icon">🎓</span>
                            ${res.degree}
                        </span>
                        <span class="meta-tag">
                            <span class="meta-icon">💼</span>
                            ${res.experience || 'Not specified'}
                        </span>
                    </div>

                    <div class="skills-display">
                        <div class="skills-group">
                            <div class="skills-label">💻 Technical Skills</div>
                            <div class="skills-container">
                                ${technicalSkillsHTML}
                            </div>
                        </div>
                        ${softSkillsHTML ? `
                        <div class="skills-group">
                            <div class="skills-label">🤝 Soft Skills</div>
                            <div class="skills-container">
                                ${softSkillsHTML}
                            </div>
                        </div>
                        ` : ''}
                    </div>
                    
                    <div class="keywords-section">
                        <div class="section-label">
                            ${res.missing_keywords.length === 0 ? 'Key Strengths' : 'Missing Skills'}
                        </div>
                        <div class="keywords-container">
                            ${keywordsHTML}
                        </div>
                    </div>
                    
                    <div class="suggestion-box ${suggestionClass}">
                        <span class="suggestion-icon">${suggestionIcon}</span>
                        <span class="suggestion-text">${suggestion}</span>
                    </div>
                </div>
                
                <div class="score-section">
                    <div class="match-strength ${scoreClass}">
                        ${res.match_strength || 'Unknown'}
                    </div>
                    <div class="score-badge ${scoreClass}">
                        ${res.score}%
                    </div>
                    <div class="score-label">Match Score</div>
                </div>
            `;
            candidatesList.appendChild(card);
        });
    }

    function renderScoreChart(scores) {
        const ctx = document.getElementById('scoreChart').getContext('2d');

        const buckets = [0, 0, 0];
        scores.forEach(s => {
            if (s < 40) buckets[0]++;
            else if (s < 80) buckets[1]++;
            else buckets[2]++;
        });

        if (scoreChartInstance) scoreChartInstance.destroy();

        scoreChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Low (<40%)', 'Medium (40-80%)', 'High (≥80%)'],
                datasets: [{
                    label: 'Candidates',
                    data: buckets,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(16, 185, 129, 0.8)'
                    ],
                    borderColor: [
                        'rgba(239, 68, 68, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(16, 185, 129, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 12,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        titleColor: '#f1f5f9',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return `${context.parsed.y} candidate${context.parsed.y !== 1 ? 's' : ''}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#94a3b8',
                            font: {
                                size: 12,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(255,255,255,0.05)',
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: '#cbd5e1',
                            font: {
                                size: 11,
                                weight: '700'
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    function renderDegreeChart(degrees) {
        const ctx = document.getElementById('degreeChart').getContext('2d');

        const counts = {};
        degrees.forEach(d => counts[d] = (counts[d] || 0) + 1);

        if (sectorChartInstance) sectorChartInstance.destroy();

        const colorPalette = [
            '#6366f1', '#ec4899', '#14b8a6', '#f59e0b',
            '#8b5cf6', '#06b6d4', '#10b981', '#f43f5e'
        ];

        sectorChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(counts),
                datasets: [{
                    data: Object.values(counts),
                    backgroundColor: colorPalette,
                    borderColor: '#0f172a',
                    borderWidth: 3,
                    hoverBorderWidth: 4,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1200,
                    easing: 'easeInOutQuart'
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#cbd5e1',
                            padding: 15,
                            font: {
                                size: 12,
                                weight: '700'
                            },
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        titleColor: '#f1f5f9',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        padding: 12,
                        callbacks: {
                            label: function (context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '65%'
            }
        });
    }
});
