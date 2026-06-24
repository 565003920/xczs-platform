import client from './client';
import type {
  Course, CourseDetail, ClassModel, ClassDetail,
  ImportResult,
  ClassProfile, ModeFingerprint, DiagnosisReport,
} from '../types';

// Courses
export const getCourses = () => client.get<Course[]>('/courses').then(r => r.data);
export const getCourse = (id: number) => client.get<CourseDetail>(`/courses/${id}`).then(r => r.data);

// Classes
export const getClasses = (courseId?: number) => {
  const params = courseId ? { course_id: courseId } : {};
  return client.get<ClassModel[]>('/classes', { params }).then(r => r.data);
};
export const getClass = (id: number) => client.get<ClassDetail>(`/classes/${id}`).then(r => r.data);

// Import
export const importCourses = (file: File) => upload('/import/courses', file);
export const importClasses = (file: File) => upload('/import/classes', file);
export const importStudents = (file: File) => upload('/import/students', file);
export const importGrades = (file: File) => upload('/import/grades', file);
export const importObservations = (file: File) => upload('/import/observations', file);
export const importEvaluations = (file: File) => upload('/import/evaluations', file);

async function upload(url: string, file: File): Promise<ImportResult> {
  const form = new FormData();
  form.append('file', file);
  return client.post<ImportResult>(url, form).then(r => r.data);
}

// Analysis
export const getClassProfile = (classId: number) =>
  client.get<ClassProfile>(`/analysis/profile/${classId}`).then(r => r.data);
export const getModeFingerprint = (classId: number) =>
  client.get<ModeFingerprint>(`/analysis/fingerprint/${classId}`).then(r => r.data);
export const getDiagnosis = (classId: number) =>
  client.get<DiagnosisReport>(`/analysis/diagnosis/${classId}`).then(r => r.data);

// Comparison (v1.5)
export const getModeComparison = (classA: number, classB: number) =>
  client.get('/analysis/compare/modes', { params: { class_a: classA, class_b: classB } }).then(r => r.data);
export const getCrossTeacherComparison = (courseId: number) =>
  client.get('/analysis/compare/cross-teacher', { params: { course_id: courseId } }).then(r => r.data);
export const getTeacherTrend = (courseId: number) =>
  client.get('/analysis/trend/teacher', { params: { course_id: courseId } }).then(r => r.data);

// Mode Library (v1.5)
export const getModeTemplates = (category?: string) =>
  client.get('/modes/templates', { params: category ? { category } : {} }).then(r => r.data);
export const getCustomModes = (courseId?: number) =>
  client.get('/modes/custom', { params: courseId ? { course_id: courseId } : {} }).then(r => r.data);
export const createCustomMode = (data: any) =>
  client.post('/modes/custom', data).then(r => r.data);
export const updateCustomMode = (id: number, data: any) =>
  client.put(`/modes/custom/${id}`, data).then(r => r.data);
export const deleteCustomMode = (id: number) =>
  client.delete(`/modes/custom/${id}`).then(r => r.data);
export const recommendModes = (classId?: number) =>
  client.get('/modes/recommend', { params: classId ? { class_id: classId } : {} }).then(r => r.data);
export const getKnowledgeGraph = (courseId: number) =>
  client.get('/modes/knowledge-graph', { params: { course_id: courseId } }).then(r => r.data);

// ── v2.0 API ──
// Student & Migration
export const getClassStudents = (classId: number) =>
  client.get(`/v2/class/${classId}/students`).then(r => r.data);
export const getStudentProfile = (studentId: number) =>
  client.get(`/v2/student/${studentId}/profile`).then(r => r.data);
export const getMigrationRecommend = (targetClassId: number) =>
  client.get('/v2/migration/recommend', { params: { target_class_id: targetClassId } }).then(r => r.data);

// Lesson Plan & Reflection
export const generateLessonPlan = (data: { class_id: number; lesson_topic: string; duration?: number }) =>
  client.post('/v2/lesson-plan/generate', data).then(r => r.data);
export const generateReflection = (data: { class_id: number; observation_id?: number }) =>
  client.post('/v2/reflection/generate', data).then(r => r.data);

// Data Assets
export const getCatalogSummary = () => client.get('/v2/catalog/summary').then(r => r.data);
export const getCatalogQuality = () => client.get('/v2/catalog/quality').then(r => r.data);
export const getDataLineageList = () => client.get('/v2/catalog/lineage').then(r => r.data);
export const getEffectivenessDashboard = () => client.get('/v2/dashboard/effectiveness').then(r => r.data);
export const getAuditLogs = (page = 1, size = 20) =>
  client.get('/v2/audit/logs', { params: { page, size } }).then(r => r.data);

// Notifications
export const getNotifications = (unreadOnly = false) =>
  client.get('/v2/notifications', { params: { unread_only: unreadOnly } }).then(r => r.data);
export const markNotificationRead = (id: number) => client.put(`/v2/notifications/${id}/read`).then(r => r.data);
export const markAllNotificationsRead = () => client.put('/v2/notifications/read-all').then(r => r.data);
