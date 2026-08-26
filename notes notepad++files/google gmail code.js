function autoDeleteNaukriAlerts() {
  // Search for Naukri alert emails older than 6 months
  var threads = GmailApp.search('from:naukrialerts@naukri.com older_than:6m');
  
  // Move them to Trash
  for (var i = 0; i < threads.length; i++) {
    threads[i].moveToTrash();
  }
}

function autoDeleteMultipleSenders() {
  // List of senders you want to clean up
  var senders = [
    'from:@linkedin.com older_than:6m',
    'from:naukrialerts@naukri.com older_than:6m',
    'from:alerts@glassdoor.com older_than:6m'
    // Add more senders here as needed
  ];
  
  // Loop through each sender query and move matching emails to Trash
  for (var i = 0; i < senders.length; i++) {
  
    var query = senders[i] + ' -is:starred';
    var threads = GmailApp.search(query);
	
    for (var j = 0; j < threads.length; j++) {
      threads[j].moveToTrash();
    }
  }
}


function autoDeleteMultipleSendersIgnoreStarred() {
  // List of senders you want to clean up
  var senders = [
    'from:@linkedin.com older_than:6m',
    'from:naukrialerts@naukri.com older_than:6m',
    'from:alerts@glassdoor.com older_than:6m'
    // Add more senders here as needed
  ];
  
  // Loop through each sender query
  for (var i = 0; i < senders.length; i++) {
    // Add "-is:starred" to ignore starred emails
    var query = senders[i] + ' -is:starred';
    
    var threads = GmailApp.search(query);
    for (var j = 0; j < threads.length; j++) {
      threads[j].moveToTrash();
    }
  }
}




function autoDeleteAllLinkedInEmails() {
  // Search for ALL emails from LinkedIn (any age), excluding starred ones
  var threads = GmailApp.search('from:@linkedin.com -is:starred');
  
  // Move them to Trash
  for (var i = 0; i < threads.length; i++) {
    threads[i].moveToTrash();
  }
}
