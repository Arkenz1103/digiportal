# 🌐 DigiPortal Custom Domain Setup

## Change from `localhost:5173` to `digiportal.local:5173`

---

## 📋 Quick Setup (Recommended)

### **Option 1: Automatic Setup (Run as Administrator)**

1. **Right-click** on `setup-domain.bat`
2. Select **"Run as Administrator"**
3. Follow the prompts
4. Restart your dev server

---

## 🔧 Manual Setup (Alternative)

### **Step 1: Edit Windows Hosts File**

1. **Open Notepad as Administrator:**
   - Press `Windows Key`
   - Type `notepad`
   - Right-click on Notepad
   - Select **"Run as administrator"**

2. **Open the hosts file:**
   - Click `File` → `Open`
   - Navigate to: `C:\Windows\System32\drivers\etc\`
   - Change file type filter to **"All Files (*.*)"**
   - Select `hosts` file
   - Click `Open`

3. **Add these lines at the bottom:**
   ```
   127.0.0.1    digiportal.local
   127.0.0.1    api.digiportal.local
   ```

4. **Save the file** (Ctrl + S)

---

### **Step 2: Restart Your Dev Server**

1. **Stop the current server:**
   - Press `Ctrl + C` in your terminal

2. **Start the server again:**
   ```bash
   npm run dev
   ```

3. **You should see:**
   ```
   VITE v5.x.x  ready in xxx ms

   ➜  Local:   http://digiportal.local:5173/
   ➜  Network: http://192.168.x.x:5173/
   ```

---

## 🚀 Access Your Application

### **New Professional URLs:**

- **Frontend:** `http://digiportal.local:5173`
- **Teacher Login:** `http://digiportal.local:5173/login`
- **Student Portal:** `http://digiportal.local:5173/student/newsfeed`
- **Teacher Dashboard:** `http://digiportal.local:5173/teacher/home`

### **Backend API:**
- **Django Admin:** `http://localhost:8000/admin`
- **API Endpoints:** `http://localhost:8000/api/`

---

## ✅ Verification

1. Open your browser
2. Go to: `http://digiportal.local:5173`
3. You should see the DigiPortal login page
4. The address bar should show: **`digiportal.local:5173`** instead of `localhost:5173`

---

## 🔄 To Remove Custom Domain (If Needed)

1. Open hosts file as Administrator (see Step 1 above)
2. Remove or comment out these lines:
   ```
   # 127.0.0.1    digiportal.local
   # 127.0.0.1    api.digiportal.local
   ```
3. Save the file
4. Restart your dev server

---

## 🎯 Benefits

✅ **Professional URL** - No more "localhost" in the address bar  
✅ **Realistic Development** - Mimics production environment  
✅ **Better Testing** - Test with a real domain structure  
✅ **Client Demos** - Show clients a professional URL  
✅ **Cookie/Session Testing** - Better domain-based testing  

---

## 🐛 Troubleshooting

### **Issue: "This site can't be reached"**
- Make sure you ran the setup as Administrator
- Check if the hosts file was updated correctly
- Restart your browser
- Clear browser cache (Ctrl + Shift + Delete)

### **Issue: Still shows localhost**
- Make sure you restarted the dev server after setup
- Try accessing: `http://digiportal.local:5173` directly
- Check if port 5173 is not blocked by firewall

### **Issue: Hot Module Replacement (HMR) not working**
- This is normal with custom domains
- Just refresh the page manually (F5)
- Or use `localhost:5173` for development and `digiportal.local:5173` for demos

---

## 📝 Notes

- The custom domain only works on your local machine
- Other devices on your network will still use your IP address
- For production, you'll need a real domain name and hosting
- The `:5173` port is still visible (this is normal for development)

---

## 🎓 Next Steps

After setup, you can:
1. Share the URL with team members (they need to do the same setup)
2. Use it for client demos
3. Test domain-specific features
4. Practice deployment workflows

---

**Need help?** Check the main README.md or contact the development team.
