// Firebase Storage Rules for Fluxor
// Copy and paste these rules in Firebase Console > Storage > Rules

rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Allow authenticated users to upload ID verification documents
    match /id-verification/{userId}/{fileName} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Allow authenticated users to upload profile images
    match /profile-images/{userId}/{fileName} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Allow public read access to verified documents (optional)
    match /verified-documents/{fileName} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Allow authenticated users to upload any file to their own folder
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
