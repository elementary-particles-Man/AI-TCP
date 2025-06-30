use std::time::Duration;

// Constants for the AIMD (Additive Increase, Multiplicative Decrease) algorithm
const INITIAL_DELAY_MS: u64 = 100;   // Initial delay, slightly higher for unpredictable networks
const MIN_DELAY_MS: u64 = 20;      // Minimum delay
const MAX_DELAY_MS: u64 = 5000;    // Maximum delay (5 seconds)
const ADDITIVE_INCREASE_MS: u64 = 10;  // Decrease delay by 10ms on success
const MULTIPLICATIVE_DECREASE_FACTOR: f64 = 1.8; // Increase delay by 80% on failure

/// Manages the sending rate adaptively based on network conditions.
pub struct RateController {
    current_delay: Duration,
}

impl RateController {
    /// Creates a new RateController with an initial delay.
    pub fn new() -> Self {
        RateController {
            current_delay: Duration::from_millis(INITIAL_DELAY_MS),
        }
    }

    /// Call this method when a packet transmission is successful.
    /// Decreases the delay additively, ensuring it doesn't go below MIN_DELAY_MS.
    pub fn on_success(&mut self) {
        let new_delay_ms = self.current_delay.as_millis() as u64 - ADDITIVE_INCREASE_MS;
        self.current_delay = Duration::from_millis(new_delay_ms.max(MIN_DELAY_MS));
    }

    /// Call this method when a packet transmission fails (e.g., timeout, NACK).
    /// Increases the delay multiplicatively, ensuring it doesn't exceed MAX_DELAY_MS.
    pub fn on_failure(&mut self) {
        let new_delay_ms = (self.current_delay.as_millis() as f64 * MULTIPLICATIVE_DECREASE_FACTOR) as u64;
        self.current_delay = Duration::from_millis(new_delay_ms.min(MAX_DELAY_MS));
    }

    /// Returns the current recommended delay that should be waited before sending the next packet.
    pub fn get_send_delay(&self) -> Duration {
        self.current_delay
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_state() {
        let controller = RateController::new();
        assert_eq!(controller.get_send_delay(), Duration::from_millis(INITIAL_DELAY_MS));
    }

    #[test]
    fn test_rate_adjustment_logic() {
        let mut controller = RateController::new();
        
        // Simulate a network failure (e.g., timeout on mesh network)
        controller.on_failure();
        let expected_delay_after_failure = (INITIAL_DELAY_MS as f64 * MULTIPLICATIVE_DECREASE_FACTOR) as u64;
        assert_eq!(controller.get_send_delay(), Duration::from_millis(expected_delay_after_failure));

        // Simulate a successful transmission after recovery
        controller.on_success();
        let expected_delay_after_success = expected_delay_after_failure - ADDITIVE_INCREASE_MS;
        assert_eq!(controller.get_send_delay(), Duration::from_millis(expected_delay_after_success));
    }
}
