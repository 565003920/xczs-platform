// ---- Base Models ----
export interface Course {
  id: number;
  name: string;
  code: string;
  department?: string;
  credits: number;
  teacher_name?: string;
  semester?: string;
}

export interface CourseDetail extends Course {
  classes: ClassModel[];
}

export interface ClassModel {
  id: number;
  name: string;
  course_id: number;
  semester?: string;
  student_count: number;
}

export interface ClassDetail extends ClassModel {
  course?: Course;
  students: Student[];
}

export interface Student {
  id: number;
  name: string;
  student_no: string;
  class_id: number;
}

export interface Observation {
  id: number;
  class_id: number;
  date?: string;
  observer?: string;
  interaction_frequency: number;
  question_depth: number;
  student_participation: number;
  lecture_ratio: number;
  discussion_ratio: number;
  practice_ratio: number;
  teaching_style_label?: string;
  notes?: string;
}

export interface Grade {
  id: number;
  student_id: number;
  class_id: number;
  exam_name: string;
  score: number;
  knowledge_point?: string;
  max_score: number;
}

export interface Evaluation {
  id: number;
  class_id: number;
  semester?: string;
  dimension: string;
  score: number;
}

// ---- Import ----
export interface ImportResult {
  imported: number;
  errors: string[];
}

// ---- Analysis ----
export interface DimensionScores {
  knowledge_mastery: number;
  participation: number;
  interaction_quality: number;
  question_depth: number;
  practice_balance: number;
  satisfaction: number;
}

export interface KnowledgePoint {
  knowledge_point: string;
  avg_score: number;
}

export interface ClassProfile {
  class_id: number;
  class_name: string;
  course_name: string;
  teacher_name?: string;
  dimensions: DimensionScores;
  weak_points: KnowledgePoint[];
  strengths: KnowledgePoint[];
  student_count: number;
  avg_grade: number;
  grade_distribution: Record<string, number>;
}

export interface FingerprintScores {
  lecture_oriented: number;
  interactive: number;
  practice_oriented: number;
  question_level: number;
  student_centeredness: number;
}

export interface ModeFingerprint {
  class_id: number;
  fingerprint: FingerprintScores;
  mode_label: string;
  mode_description: string;
  mode_recommendations: string[];
  observation_count: number;
}

export interface DiagnosisReport {
  class_id: number;
  class_name: string;
  course_name: string;
  teacher_name?: string;
  profile: ClassProfile;
  fingerprint: ModeFingerprint;
  teaching_mode_suggestion: string;
}
