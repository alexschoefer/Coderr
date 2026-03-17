from django.db import models

class FileUpload(models.Model):
    """Model to represent a file upload."""
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the FileUpload model, showing the file name."""
        return self.file.name
