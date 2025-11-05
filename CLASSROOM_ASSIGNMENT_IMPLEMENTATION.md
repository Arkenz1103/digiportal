# 🎓 Classroom-Based Activity Assignment System

## 📋 Overview

Implemented a comprehensive classroom-based filtering system that ensures teachers can only assign activities to students in their specific assigned classroom(s), and students only see activities from their own classroom.

---

## 🔧 Changes Made

### **1. Database Model Updates**

#### **PortfolioFolder Model** (`be/api/models.py`)
Added new field to link folders to specific classrooms:

```python
class PortfolioFolder(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_folders')
    name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255, default='General')  # Legacy field
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='portfolio_folders')  # NEW FIELD
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Purpose:** Links portfolio folders directly to Classroom model instead of just using string-based class_name.

---

### **2. Folder Creation Logic** (`be/api/views.py`)

#### **Automatic Classroom Assignment**
When a teacher creates a folder, it's automatically linked to their classroom:

```python
# Get teacher's classroom based on class_name
classroom = Classroom.objects.filter(
    teacher=request.user,
    name=class_name
).first()

folder = PortfolioFolder.objects.create(
    teacher=request.user,
    name=name,
    class_name=class_name,
    classroom=classroom,  # Linked to actual Classroom
    description=description
)
```

#### **Targeted Student Notifications**
Only students in the specific classroom receive notifications:

```python
# Notify ONLY students in this specific classroom
if classroom:
    students = User.objects.filter(
        role='student',
        classroom=classroom
    ).exclude(username='admin')
    print(f"📢 Notifying {students.count()} students in {classroom.name}")
```

**Before:** All students received notifications for every folder
**After:** Only students in Grade 1-A receive notifications for Grade 1-A folders

---

### **3. Student Activity View** (`get_student_portfolio_activities_api`)

#### **Classroom-Based Filtering**
Students only see activities from their assigned classroom:

```python
# Get student's classroom
student_classroom = request.user.classroom

if not student_classroom:
    # Return empty if student has no classroom
    return Response({
        'all_activities': [],
        'submitted_activities': [],
        'missing_activities': [],
        ...
    })

# Get ONLY portfolio folders for this student's assigned classroom
folders = PortfolioFolder.objects.filter(
    classroom=student_classroom,
    class_name=class_name
)
```

**Result:** Students in Grade 1-A only see activities created for Grade 1-A

---

### **4. Teacher Submission View** (`activity_submissions_api`)

#### **Classroom-Based Submission Filtering**
Teachers only see submissions from students in the activity's classroom:

```python
# Get teacher's classroom(s) for this activity
activity_classroom = activity.folder.classroom

# Filter submissions by classroom
all_submissions = StudentSubmission.objects.filter(
    activity=activity,
    student__classroom=activity_classroom  # Only students from this classroom
).exclude(status='draft').order_by('-submitted_at')
```

**Result:** Teacher sees only submissions from their assigned students

---

## 🎯 How It Works

### **Scenario: Teacher Maria Santos (Grade 1-A)**

#### **1. Creating Activities**
```
Teacher: Maria Santos
Assigned Classroom: Grade 1 - Section A
Action: Creates "Science" folder

Result:
✅ Folder linked to "Grade 1 - Section A" classroom
✅ Only 30 students in Grade 1-A notified
❌ Students in Grade 2-B, Grade 3-C NOT notified
```

#### **2. Student View**
```
Student: Noah Aguilar
Assigned Classroom: Grade 1 - Section A

Portfolio View Shows:
✅ Science folder (created by Maria Santos for Grade 1-A)
✅ Mapeh folder (created by Maria Santos for Grade 1-A)
❌ Math folder (created by different teacher for Grade 2-B)
```

#### **3. Teacher Viewing Submissions**
```
Teacher: Maria Santos
Viewing: Science Activity #5

Submissions Shown:
✅ Noah Aguilar (Grade 1-A)
✅ Bridget Aquino (Grade 1-A)
✅ Celeste Aquino (Grade 1-A)
❌ Students from other classrooms NOT shown
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    TEACHER CREATES FOLDER                    │
│                                                              │
│  Teacher: Maria Santos                                       │
│  Classroom: Grade 1 - A                                      │
│  Folder: "Science"                                           │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              SYSTEM LINKS FOLDER TO CLASSROOM                │
│                                                              │
│  PortfolioFolder {                                           │
│    name: "Science",                                          │
│    teacher: Maria Santos,                                    │
│    classroom: Grade 1-A (FK),                                │
│    class_name: "Grade 1 - A"                                 │
│  }                                                           │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│            NOTIFY ONLY STUDENTS IN CLASSROOM                 │
│                                                              │
│  Query: User.objects.filter(                                 │
│           role='student',                                    │
│           classroom=Grade 1-A                                │
│         )                                                    │
│                                                              │
│  Result: 30 students notified                                │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              STUDENTS SEE ONLY THEIR ACTIVITIES              │
│                                                              │
│  Student: Noah Aguilar (Grade 1-A)                           │
│  Sees: All folders where classroom = Grade 1-A               │
│  Doesn't See: Folders for other classrooms                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security & Access Control

### **Access Rules**

| User Type | Can See | Cannot See |
|-----------|---------|------------|
| **Teacher (Grade 1-A)** | - Own classroom folders<br>- Submissions from Grade 1-A students | - Other teachers' folders<br>- Submissions from other classrooms |
| **Student (Grade 1-A)** | - Activities from Grade 1-A<br>- Own submissions | - Activities from other grades<br>- Other students' submissions |
| **Admin** | - All classrooms<br>- All submissions | N/A |

---

## 📝 Migration Steps

### **1. Create Migration**
```bash
cd c:\Users\ACER\Downloads\digiportal\be
python manage.py makemigrations
```

Expected output:
```
Migrations for 'api':
  api/migrations/0XXX_add_classroom_to_portfoliofolder.py
    - Add field classroom to portfoliofolder
```

### **2. Run Migration**
```bash
python manage.py migrate
```

### **3. Link Existing Folders (Optional)**
Run this script to link existing folders to classrooms:

```python
from api.models import PortfolioFolder, Classroom

# Link folders to classrooms based on class_name
folders = PortfolioFolder.objects.filter(classroom__isnull=True)

for folder in folders:
    classroom = Classroom.objects.filter(
        teacher=folder.teacher,
        name=folder.class_name
    ).first()
    
    if classroom:
        folder.classroom = classroom
        folder.save()
        print(f"✅ Linked {folder.name} to {classroom.name}")
    else:
        print(f"⚠️ No classroom found for {folder.class_name}")
```

---

## ✅ Benefits

### **For Teachers:**
1. **Organized Management**: Only see relevant students
2. **Accurate Tracking**: No confusion with other classrooms
3. **Targeted Communication**: Notifications go to right students
4. **Efficient Grading**: Only grade assigned students

### **For Students:**
1. **Relevant Content**: Only see their own activities
2. **Clear Expectations**: No confusion with other classes
3. **Focused Learning**: Activities match their grade level
4. **Privacy**: Don't see other classrooms' work

### **For System:**
1. **Data Integrity**: Proper relational database structure
2. **Scalability**: Easy to add more classrooms
3. **Performance**: Filtered queries are faster
4. **Maintainability**: Clear data relationships

---

## 🧪 Testing Checklist

### **Teacher Tests:**
- [ ] Create folder for Grade 1-A
- [ ] Verify only Grade 1-A students notified
- [ ] View submissions - only Grade 1-A students shown
- [ ] Create activity - only Grade 1-A students can submit
- [ ] Check Remarks page - only Grade 1-A students listed

### **Student Tests:**
- [ ] Login as Grade 1-A student
- [ ] Verify only Grade 1-A activities visible
- [ ] Try to access Grade 2-B activity (should fail)
- [ ] Submit work - appears only to Grade 1-A teacher
- [ ] Check portfolio - only Grade 1-A activities shown

### **Cross-Classroom Tests:**
- [ ] Teacher A creates activity for Grade 1-A
- [ ] Teacher B creates activity for Grade 2-B
- [ ] Verify Grade 1-A students don't see Grade 2-B activities
- [ ] Verify Grade 2-B students don't see Grade 1-A activities
- [ ] Verify teachers only see their own students' submissions

---

## 🚀 Future Enhancements

1. **Multi-Classroom Teachers**: Support teachers assigned to multiple classrooms
2. **Classroom Transfer**: Move students between classrooms
3. **Shared Activities**: Allow activities to be shared across classrooms
4. **Classroom Analytics**: Per-classroom performance reports
5. **Classroom Archives**: Archive completed school years

---

## 📞 Support

If you encounter issues:
1. Check student has assigned classroom
2. Verify teacher is assigned to classroom
3. Check folder has classroom link
4. Review migration status
5. Check console logs for debugging info

---

## 🎉 Summary

The classroom-based assignment system ensures:
- ✅ **Teachers** only manage their assigned students
- ✅ **Students** only see relevant activities
- ✅ **Activities** are properly scoped to classrooms
- ✅ **Notifications** reach the right audience
- ✅ **Data** is organized and secure

This creates a **professional, organized, and efficient** learning management system! 🎓✨
