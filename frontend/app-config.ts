export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Teach-the-Tutor',
  pageTitle: 'Active Recall Learning Coach',
  pageDescription: 'Master programming concepts through interactive learning modes',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#3b82f6',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#60a5fa',
  startButtonText: 'Start Learning',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
