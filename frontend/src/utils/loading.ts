/**
 * 로딩 상태 관리 유틸리티
 */

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

/**
 * 로딩 상태를 관리하는 간단한 클래스
 */
export class LoadingManager {
  private loadingStates: Map<string, boolean> = new Map();
  private errorStates: Map<string, string | null> = new Map();

  setLoading(key: string, isLoading: boolean): void {
    this.loadingStates.set(key, isLoading);
    if (!isLoading) {
      this.errorStates.set(key, null);
    }
  }

  setError(key: string, error: string | null): void {
    this.errorStates.set(key, error);
    if (error) {
      this.loadingStates.set(key, false);
    }
  }

  isLoading(key: string): boolean {
    return this.loadingStates.get(key) ?? false;
  }

  getError(key: string): string | null {
    return this.errorStates.get(key) ?? null;
  }

  getState(key: string): LoadingState {
    return {
      isLoading: this.isLoading(key),
      error: this.getError(key),
    };
  }

  clear(key: string): void {
    this.loadingStates.delete(key);
    this.errorStates.delete(key);
  }

  clearAll(): void {
    this.loadingStates.clear();
    this.errorStates.clear();
  }
}

