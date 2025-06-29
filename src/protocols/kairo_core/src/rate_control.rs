use std::time::Duration;

const INITIAL_DELAY_MS: u64 = 1000; // 1 second
const MIN_DELAY_MS: u64 = 100;     // 100 milliseconds
const MAX_DELAY_MS: u64 = 10000;   // 10 seconds

const ADDITIVE_INCREASE_MS: u64 = 50; // For success
const MULTIPLICATIVE_DECREASE_FACTOR: f64 = 1.5; // For failure

pub struct RateController {
    current_delay: Duration,
}

impl RateController {
    pub fn new() -> Self {
        RateController {
            current_delay: Duration::from_millis(INITIAL_DELAY_MS),
        }
    }

    // Called on successful packet transmission
    pub fn on_success(&mut self) {
        let new_delay_ms = self.current_delay.as_millis()
            .saturating_sub(ADDITIVE_INCREASE_MS as u128)
            .max(MIN_DELAY_MS as u128);
        self.current_delay = Duration::from_millis(new_delay_ms as u64);
    }

    // Called on packet loss or timeout
    pub fn on_failure(&mut self) {
        let new_delay_ms = (self.current_delay.as_millis() as f64 * MULTIPLICATIVE_DECREASE_FACTOR)
            .min(MAX_DELAY_MS as f64) as u128;
        self.current_delay = Duration::from_millis(new_delay_ms as u64);
    }
    
    pub fn get_send_delay(&self) -> Duration {
        self.current_delay
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rate_adjustment() {
        let mut controller = RateController::new();
        assert_eq!(controller.get_send_delay(), Duration::from_millis(INITIAL_DELAY_MS));

        // On failure, delay should increase
        controller.on_failure();
        let expected_delay_after_failure = (INITIAL_DELAY_MS as f64 * MULTIPLICATIVE_DECREASE_FACTOR).min(MAX_DELAY_MS as f64) as u64;
        assert_eq!(controller.get_send_delay(), Duration::from_millis(expected_delay_after_failure));

        // On success, delay should decrease
        controller.on_success();
        let expected_delay_after_success = (expected_delay_after_failure as u128).saturating_sub(ADDITIVE_INCREASE_MS as u128).max(MIN_DELAY_MS as u128) as u64;
        assert_eq!(controller.get_send_delay(), Duration::from_millis(expected_delay_after_success));

        // Test min delay
        let mut controller_min = RateController::new();
        controller_min.current_delay = Duration::from_millis(MIN_DELAY_MS);
        controller_min.on_success();
        assert_eq!(controller_min.get_send_delay(), Duration::from_millis(MIN_DELAY_MS));

        // Test max delay
        let mut controller_max = RateController::new();
        controller_max.current_delay = Duration::from_millis(MAX_DELAY_MS);
        controller_max.on_failure();
        assert_eq!(controller_max.get_send_delay(), Duration::from_millis(MAX_DELAY_MS));
    }
}
