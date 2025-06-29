use lz4_flex::{compress_prepend_size, decompress_size_prepended};

/// Compresses data using LZ4 with a prepended size.
pub fn compress(data: &[u8]) -> Vec<u8> {
    compress_prepend_size(data)
}

/// Decompresses data using LZ4, reading the size from the prefix.
pub fn decompress(compressed_data: &[u8]) -> Result<Vec<u8>, lz4_flex::block::DecompressError> {
    decompress_size_prepended(compressed_data)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compression_decompression() {
        let original_data = b"Hello, world! This is a test string for LZ4 compression.";
        let compressed_data = compress(original_data);
        let decompressed_data = decompress(&compressed_data).expect("Decompression failed");
        assert_eq!(original_data.to_vec(), decompressed_data);
    }

    #[test]
    fn test_empty_payload() {
        let original_data = b"";
        let compressed_data = compress(original_data);
        let decompressed_data = decompress(&compressed_data).expect("Decompression of empty payload failed");
        assert_eq!(original_data.to_vec(), decompressed_data);
    }
}