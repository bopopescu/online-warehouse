import { TestBed } from '@angular/core/testing';

import { TrackingService } from './tracking.service';

describe('TrackingService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TrackingService]
    });
  });

  it('should be created', () => {
    const service: TrackingService = TestBed.get(TrackingService);
    expect(service).toBeTruthy();
  });
});
