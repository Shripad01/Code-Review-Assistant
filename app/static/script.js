// Wait for the entire HTML document to be fully loaded and parsed.
document.addEventListener('DOMContentLoaded', () => {

    // Get references to the key HTML elements we need to interact with.
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');
    const reportContent = document.getElementById('reportContent');
    const reportTitle = document.getElementById('report-title');
    const fileLabel = document.querySelector('.file-label');

    // Add an event listener to the file input to update the label text
    // when a file is chosen.
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileLabel.textContent = fileInput.files[0].name;
        } else {
            fileLabel.textContent = 'Choose a File';
        }
    });

    // Add a 'click' event listener to the submit button.
    submitBtn.addEventListener('click', async () => {
        // Check if a file has been selected by the user.
        if (fileInput.files.length === 0) {
            alert('Please select a file first!');
            return; // Stop the function if no file is selected.
        }

        // Get the first file from the FileList object.
        const file = fileInput.files[0];

        // Create a FormData object to easily handle file uploads.
        const formData = new FormData();
        formData.append('file', file);

        // Update the UI to show that the analysis is in progress.
        reportTitle.innerHTML = `<span class="loading"></span>Reviewing ${file.name}...`;
        reportContent.innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <div class="loading" style="margin: 0 auto 1rem;"></div>
                <p>Analyzing your code. This may take a moment...</p>
                <p style="color: #666; font-size: 0.9rem;">Processing ${file.name} (${Math.round(file.size / 1024)} KB)</p>
            </div>
        `;
        submitBtn.disabled = true; // Disable button to prevent multiple submissions
        submitBtn.innerHTML = '<span class="loading"></span>Analyzing...';


        try {
            // Use the Fetch API to send a POST request to our backend endpoint.
            const response = await fetch('/review/', {
                method: 'POST',
                body: formData, // The FormData object is the body of our request.
            });

            // Parse the JSON response from the server.
            const result = await response.json();
            
            // Debug logging
            console.log('Response status:', response.status);
            console.log('Response data:', result);
            console.log('Review report type:', typeof result.review_report);
            console.log('Review report keys:', result.review_report ? Object.keys(result.review_report) : 'No review_report');

            // Check if the HTTP response status is not OK (e.g., 400 or 500).
            if (!response.ok) {
                // If the server provided a specific error detail, use it.
                // Otherwise, throw a generic error.
                throw new Error(result.detail || 'An unknown error occurred on the server.');
            }

            // Check if the response has the expected structure
            if (!result.review_report) {
                console.error('Unexpected response structure:', result);
                reportContent.innerHTML = `
                    <div class="error-message">
                        <h3>âš ï¸ Unexpected Response Format</h3>
                        <p>The server returned an unexpected response format. Please try again.</p>
                        <details>
                            <summary>Debug Information</summary>
                            <pre>${JSON.stringify(result, null, 2)}</pre>
                        </details>
                    </div>
                `;
                return;
            }

            // Try to display the structured report, with fallback to raw JSON
            try {
                displayReviewReport(result);
            } catch (error) {
                console.error('Error in displayReviewReport:', error);
                console.error('Error details:', error.stack);
                // Fallback to displaying raw JSON
                reportContent.innerHTML = `
                    <div class="error-message">
                        <h3>âš ï¸ Display Error</h3>
                        <p>There was an error displaying the review. Error: ${error.message}</p>
                        <details>
                            <summary>Raw Response Data</summary>
                            <pre>${JSON.stringify(result, null, 2)}</pre>
                        </details>
                    </div>
                `;
            }

        } catch (error) {
            // If any error occurs during the fetch process, display it.
            reportContent.textContent = `Error: ${error.message}`;
            reportTitle.textContent = 'Review Report'; // Reset title on error
        } finally {
            // This block will run regardless of whether there was an error or not.
            submitBtn.disabled = false; // Re-enable the button
            submitBtn.innerHTML = 'Get Review';
        }
    });

    // Function to display the comprehensive review report
    function displayReviewReport(result) {
        try {
            const review = result.review_report;
            
            // Validate that we have the required data
            if (!review) {
                throw new Error('No review data found in response');
            }
            
            console.log('Review data:', review);
        
        // Update the title with file info
        reportTitle.innerHTML = `
            <span class="file-info">ðŸ“„ ${result.filename}</span>
            <span class="processing-info">â±ï¸ ${result.processing_time_ms}ms | ðŸ¤– ${result.model_used || 'Unknown Model'}</span>
        `;

        // Create comprehensive HTML report
        let html = `
            <div class="review-summary">
                <div class="summary-header">
                    <h2>ðŸ“Š Code Review Summary</h2>
                    <div class="overall-score ${getScoreClass(review.overall_score)}">
                        ${review.overall_score}/100
                    </div>
                </div>
                <p class="summary-text">${review.overall_summary}</p>
            </div>

            <div class="execution-analysis">
                <h3>ðŸ” Execution Analysis</h3>
                <div class="analysis-grid">
                    <div class="analysis-item ${review.execution_analysis.will_compile ? 'success' : 'error'}">
                        <span class="icon">${review.execution_analysis.will_compile ? 'âœ…' : 'âŒ'}</span>
                        <span class="label">Compilation</span>
                        <span class="status">${review.execution_analysis.will_compile ? 'Will Compile' : 'Won\'t Compile'}</span>
                    </div>
                    <div class="analysis-item ${review.execution_analysis.will_run ? 'success' : 'error'}">
                        <span class="icon">${review.execution_analysis.will_run ? 'âœ…' : 'âŒ'}</span>
                        <span class="label">Runtime</span>
                        <span class="status">${review.execution_analysis.will_run ? 'Will Run' : 'Won\'t Run'}</span>
                    </div>
                    <div class="analysis-item ${review.has_critical_issues ? 'warning' : 'success'}">
                        <span class="icon">${review.has_critical_issues ? 'âš ï¸' : 'âœ…'}</span>
                        <span class="label">Critical Issues</span>
                        <span class="status">${review.has_critical_issues ? 'Yes' : 'No'}</span>
                    </div>
                </div>
                <div class="expected-behavior">
                    <strong>Expected Behavior:</strong> ${review.execution_analysis.expected_behavior}
                </div>
            </div>

            <div class="quality-metrics">
                <h3>ðŸ“ˆ Quality Metrics</h3>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-label">Readability</div>
                        <div class="metric-bar">
                            <div class="metric-fill" style="width: ${review.quality_metrics.readability * 10}%"></div>
                        </div>
                        <div class="metric-score">${review.quality_metrics.readability}/10</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Efficiency</div>
                        <div class="metric-bar">
                            <div class="metric-fill" style="width: ${review.quality_metrics.efficiency * 10}%"></div>
                        </div>
                        <div class="metric-score">${review.quality_metrics.efficiency}/10</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Maintainability</div>
                        <div class="metric-bar">
                            <div class="metric-fill" style="width: ${review.quality_metrics.maintainability * 10}%"></div>
                        </div>
                        <div class="metric-score">${review.quality_metrics.maintainability}/10</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Security</div>
                        <div class="metric-bar">
                            <div class="metric-fill" style="width: ${review.quality_metrics.security * 10}%"></div>
                        </div>
                        <div class="metric-score">${review.quality_metrics.security}/10</div>
                    </div>
                </div>
            </div>
        `;

        // Add issues section if there are any
        if (review.issues && review.issues.length > 0) {
            html += `
                <div class="issues-section">
                    <h3>ðŸ› Issues Found (${review.issues.length})</h3>
                    <div class="issues-list">
            `;

            // Group issues by priority
            const highPriorityIssues = review.issues.filter(issue => issue.priority === 'High');
            const mediumPriorityIssues = review.issues.filter(issue => issue.priority === 'Medium');
            const lowPriorityIssues = review.issues.filter(issue => issue.priority === 'Low');

            // Display issues by priority
            [highPriorityIssues, mediumPriorityIssues, lowPriorityIssues].forEach((issues, index) => {
                const priorityNames = ['High', 'Medium', 'Low'];
                const priorityClasses = ['high', 'medium', 'low'];
                
                if (issues.length > 0) {
                    html += `
                        <div class="priority-group ${priorityClasses[index]}">
                            <h4 class="priority-header">${priorityNames[index]} Priority (${issues.length})</h4>
                    `;
                    
                    issues.forEach(issue => {
                        html += `
                            <div class="issue-item">
                                <div class="issue-header">
                                    <span class="issue-line">Line ${issue.line}</span>
                                    <span class="issue-category">${issue.category}</span>
                                    <span class="issue-priority ${issue.priority.toLowerCase()}">${issue.priority}</span>
                                </div>
                                <div class="issue-title">${issue.title}</div>
                                <div class="issue-description">${formatMarkdown(issue.description)}</div>
                                <div class="issue-impact"><strong>Impact:</strong> ${issue.potential_impact}</div>
                                <div class="issue-tags">
                                    ${issue.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                </div>
                                <details class="issue-fix">
                                    <summary>ðŸ’¡ Suggested Fix</summary>
                                    <div class="fix-content">${formatMarkdown(issue.suggested_fix)}</div>
                                </details>
                            </div>
                        `;
                    });
                    
                    html += `</div>`;
                }
            });

            html += `
                    </div>
                </div>
            `;
        } else {
            html += `
                <div class="no-issues">
                    <h3>ðŸŽ‰ No Issues Found!</h3>
                    <p>Great job! Your code looks clean and well-written.</p>
                </div>
            `;
        }

        // Set the HTML content
        reportContent.innerHTML = html;
        
        } catch (error) {
            console.error('Error displaying review report:', error);
            reportContent.innerHTML = `
                <div class="error-message">
                    <h3>âš ï¸ Error Displaying Review</h3>
                    <p>There was an error displaying the review report: ${error.message}</p>
                    <details>
                        <summary>Debug Information</summary>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    </details>
                </div>
            `;
        }
    }

    // Helper function to get CSS class based on score
    function getScoreClass(score) {
        if (score >= 80) return 'excellent';
        if (score >= 60) return 'good';
        if (score >= 40) return 'fair';
        return 'poor';
    }

    // Helper function to format basic markdown
    function formatMarkdown(text) {
        if (!text) return '';
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    // Test function to verify display works
    function testDisplay() {
        const testData = {
            filename: "test.py",
            processing_time_ms: 1000,
            model_used: "gemini-2.5-flash",
            review_report: {
                language: "Python",
                overall_summary: "This is a test review summary.",
                execution_analysis: {
                    will_compile: true,
                    will_run: true,
                    expected_behavior: "The code will run successfully."
                },
                has_critical_issues: false,
                overall_score: 85,
                quality_metrics: {
                    readability: 8,
                    efficiency: 7,
                    maintainability: 9,
                    security: 6
                },
                issues: [
                    {
                        line: 1,
                        priority: "Medium",
                        category: "Best Practice",
                        tags: ["test-tag"],
                        title: "Test Issue",
                        description: "This is a test issue description.",
                        potential_impact: "Test impact",
                        suggested_fix: "Test fix suggestion"
                    }
                ]
            }
        };
        
        console.log("Testing display with sample data...");
        displayReviewReport(testData);
    }

    // Uncomment the line below to test the display function
    // testDisplay();
});