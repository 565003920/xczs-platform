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
