use lz4_flex::{compress_into, decompress_into, decompress_size_prepended};

pub fn compress(input: &[u8]) -> Vec<u8> {
    lz4_flex::compress_prepend_size(input)
}

pub fn decompress(input: &[u8]) -> Result<Vec<u8>, lz4_flex::block::DecompressError> {
    lz4_flex::decompress_size_prepended(input)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compression_decompression() {
        let original = b"Hello, world! This is a test string for LZ4 compression.";
        let compressed = compress(original);
        let decompressed = decompress(&compressed).unwrap();
        assert_eq!(original.to_vec(), decompressed);
    }

    #[test]
    fn test_empty_data() {
        let original = b"";
        let compressed = compress(original);
        let decompressed = decompress(&compressed).unwrap();
        assert_eq!(original.to_vec(), decompressed);
    }

    #[test]
    fn test_long_data() {
        let original = b"".repeat(1024 * 10).into_bytes(); // 10KB of zeros
        let compressed = compress(&original);
        let decompressed = decompress(&compressed).unwrap();
        assert_eq!(original.to_vec(), decompressed);
    }
}
